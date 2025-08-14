# ChannelMessageMasking

## 概要
ChannelMessageMaskingはTeamsのチャネルからエクスポートしたメッセージデータのマスキング（個人情報や機密情報の検出・置換）を行うPythonベースのツールです。

## 主な機能
- テキストデータから個人情報（PII）を検出
- 検出した情報のマスキング・置換

## ファイル構成
- masking.py : マスキング処理のメインロジック
- aiservice.py : Azure AI Service連携用モジュール
- presidio.py : Presidio連携用モジュール
- run-aiservice.py : Azure AI Serviceコンテナ実行用スクリプト
- config.ini : 設定ファイル

## 設定ファイル
[Azure AI SERVICE]  
ENDPOINT_URI：Azure AI サービスエンドポイント  
API_KEY：Azure AI サービスAPIキー  

[CONTAINER]  
ENDPOINT_URI：Azure AI サービスコンテナエンドポイント  
IMAGE_TAG：Azure AI サービスコンテナのイメージタグ  

[MODEL]  
LANG_CODE：Presidioで使用するモデルの言語コード  
MODEL_NAME：Presidioで使用するモデル名  

## 使い方
1. 必要なPythonパッケージをインストール  
   ```pip install -r requirements.txt```
2. 設定ファイル (config.ini) を編集
3. Azure AI サービスを使用する場合はコンテナ起動  
   ```python run-aiservice.py```
4. マスキング処理を実行  
   ```python masking.py "ファイルパス"```

## Azure AI Serviceの準備
1. Docker環境の構築
2. [Azure AI Faundry (旧Azure AI Service) リソースの作成](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal)
3. エンドポイントとAPIキーを設定ファイルに登録

## spaCyモデルの準備
1. [公式ドキュメント](https://spacy.io/models/ja#ja_core_news_trf)を参照してモデルをインストール

## 作者
- Kotaro Harada（NTT DATA INTELLILINK Corporation）

