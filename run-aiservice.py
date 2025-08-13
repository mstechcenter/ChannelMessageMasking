import configparser
config_ini = configparser.ConfigParser()
config_ini.read("config.ini.local", encoding="utf-8")
import subprocess

IMAGE_TAG = config_ini["CONTAINER"]["IMAGE_TAG"]
ENDPOINT_URI = config_ini["Azure AI SERVICE"]["ENDPOINT_URI"]
API_KEY = config_ini["Azure AI SERVICE"]["API_KEY"]

CMD = f"wsl.exe docker run --rm -it -p 5000:5000 --memory 8g --cpus 1 \
mcr.microsoft.com/azure-cognitive-services/textanalytics/pii:{IMAGE_TAG} \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}"

# print(CMD)
subprocess.run(CMD)