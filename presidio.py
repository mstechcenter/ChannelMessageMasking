import configparser
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngineProvider

# 設定ファイルからモデルを読み込み
config_ini = configparser.ConfigParser()
config_ini.read("config.ini.local", encoding="utf-8")
lang_code = config_ini["MODEL"]["LANG_CODE"]
model_name = config_ini["MODEL"]["MODEL_NAME"]

configuration = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": lang_code, "model_name": model_name},
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