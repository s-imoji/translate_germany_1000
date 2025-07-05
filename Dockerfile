# ベースイメージとしてPython 3.9の軽量版を使用
FROM python:3.9-slim

# 環境変数を設定（コンテナ内のログがバッファリングされないようにする）
ENV PYTHONUNBUFFERED True

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルを先にコピーし、キャッシュを活用
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードを全てコピー
COPY . .

# Cloud Runから渡されるPORT環境変数をリッスンするGunicornを起動
# gunicorn <WSGIサーバー>:<Flaskインスタンス名>
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
