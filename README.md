# Flask Real-time Translator

日本語または英語のテキストをリアルタイムでドイツ語に翻訳するWebアプリケーションです。
Google Cloud Runへのデプロイを想定しています。

## 構成
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla JS)
- **Translation**: `deep-translator` library
- **Deployment**: Docker, Google Cloud Run

## ローカルでの実行方法

1.  **リポジトリをクローン**
    ```bash
    git clone https://github.com/s-imoji/s-imoji-translator.git
    cd s-imoji-translator
    ```

2.  **Python仮想環境の作成と有効化**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **依存ライブラリのインストール**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Flaskアプリケーションの実行**
    ```bash
    python main.py
    ```

5.  ブラウザで `http://127.0.0.1:8080` にアクセスします。

## Google Cloud Runへのデプロイ手順

1.  **Google Cloud SDKをインストール**し、初期設定を完了させます。
    - `gcloud auth login`
    - `gcloud config set project [YOUR_PROJECT_ID]`

2.  **Artifact Registry APIを有効化**します。

3.  **コンテナイメージをビルドし、Artifact Registryにプッシュ**します。
    ```bash
    gcloud builds submit --tag gcr.io/[YOUR_PROJECT_ID]/translator-app
    ```
    ※ `[YOUR_PROJECT_ID]` はご自身のGCPプロジェクトIDに置き換えてください。

4.  **ビルドしたイメージをCloud Runにデプロイ**します。
    ```bash
    gcloud run deploy translator-service \
      --image gcr.io/[YOUR_PROJECT_ID]/translator-app \
      --platform managed \
      --region asia-northeast1 \
      --allow-unauthenticated
    ```
    - `translator-service` は任意のサービス名に変更可能です。
    - `--region` は適切なリージョンを指定してください（例: `asia-northeast1` (東京)）。
    - `--allow-unauthenticated` をつけることで、誰でもHTTPSでアクセスできるようになります。

デプロイが完了すると、コンソールに `Service [translator-service] revision [translator-service-XXXXX-xxx] has been deployed and is serving 100% of traffic at https://....run.app` のようなメッセージが表示されます。このURLにブラウザでアクセスすれば、アプリケーションが利用できます。
