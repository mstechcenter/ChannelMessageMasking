import sys
import json
import re
import configparser
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngineProvider

configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "ja", "model_name": "ja_core_news_trf"},
    ],
}

# クライアントは1度だけ生成し、全関数で共有
analyzer = None
def get_analyzer():
    global analyzer
    if analyzer is None:
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()
        analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine, supported_languages=["ja"]
        )      
    return analyzer

anonymizer = None
def get_anonymizer():
    global anonymizer
    if anonymizer is None:
        anonymizer = AnonymizerEngine()        
    return anonymizer

# PII検出・マスキング
def pii_recognition(value):
    print("Source Text: {}".format(value))

    analyzer = get_analyzer()
    analyzer_result = analyzer.analyze(
        text=value,
        language="ja"   
    )

    anonymizer = get_anonymizer()
    anonymizer_result = anonymizer.anonymize(
        text=value,
        analyzer_results=analyzer_result,
        operators={"PERSON": OperatorConfig("mask", {"type": "mask", "masking_char" : "*", "chars_to_mask" : 5, "from_end" : True}),
                   "ORGANIZATION": OperatorConfig("mask", {"type": "mask", "masking_char" : "*", "chars_to_mask" : 5, "from_end" : True})
            }
    )

    print("Redacted Text: {}".format(anonymizer_result.text))
    return anonymizer_result.text if anonymizer_result else value

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