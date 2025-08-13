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