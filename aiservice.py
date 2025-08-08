import sys
import json
import re
import configparser
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# 設定ファイルからAPIキーとエンドポイントを取得
config_ini = configparser.ConfigParser()
config_ini.read("config.ini.local", encoding="utf-8")
language_key = config_ini["Azure AI SERVICE"]["API_KEY"]
language_endpoint = config_ini["CONTAINER"]["ENDPOINT_URI"]

# クライアントは1度だけ生成し、全関数で共有
piiclient = None
def get_piiclient():
    global piiclient
    if piiclient is None:
        ta_credential = AzureKeyCredential(language_key)
        piiclient = TextAnalyticsClient(endpoint=language_endpoint, credential=ta_credential)
    return piiclient

# PII検出・マスキング
def pii_recognition(value):
    print("Source Text: {}".format(value))

    client = get_piiclient()
    doc = [value]
    response = client.recognize_pii_entities(doc, language="ja")

    print("Redacted Text: {}".format(response[0].redacted_text))
    return response[0].redacted_text if response and not response[0].is_error else value

# マスキング処理
def mask_value(value, key=None):    
    if isinstance(value, str):
        if key in ('displayName', 'mentionText', 'content'):
            return pii_recognition(value)
        else:
            value = re.sub(r'[0-9a-fA-F\-]{36}', '*****', value)
            return value
    else:
        return value

def mask_dict(d):
    mask_keys = ['id', 'displayName', 'userIdentityType', 'mentionText', 'content']
    if isinstance(d, dict):
        return {k: mask_dict(v) if isinstance(v, (dict, list)) else (mask_value(v, k) if k in mask_keys else v) for k, v in d.items()}
    elif isinstance(d, list):
        return [mask_dict(item) for item in d]
    else:
        return d

if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else 'testdata/testdata.json'

    with open(source, encoding='utf-8') as f:
        data = json.load(f)

    masked_data = mask_dict(data)

    with open(f'{source}_redacted', 'w', encoding='utf-8') as f:
        json.dump(masked_data, f, ensure_ascii=False, indent=2)