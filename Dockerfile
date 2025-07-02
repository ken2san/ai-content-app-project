# Pythonの公式イメージをベースにする
FROM python:3.9-slim-buster

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 必要なシステム依存関係とFFmpegをインストール
# Pillowが画像生成時に使うフォントも追加 (fontconfigとttf-dejavu-core)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ffmpeg \
    fontconfig \
    ttf-dejavu-core \
    gettext && \
    rm -rf /var/lib/apt/lists/*

# Pythonの依存関係ファイルをコンテナにコピー
COPY requirements.txt .

# Pythonの依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコンテナにコピー
COPY main.py .
COPY ai_content_automation_app.html .
COPY app/ app/

# 生成されたメディアファイルを保存するディレクトリを作成
RUN mkdir -p generated_media

# babel.cfg ファイルをコピー
COPY babel.cfg .

# Translation setup
RUN mkdir -p app/translations/en/LC_MESSAGES app/translations/ja/LC_MESSAGES

# Copy translation scripts
COPY fix_translations.sh .
COPY update_translations.sh .
RUN chmod +x fix_translations.sh update_translations.sh

# Compile translations
RUN cd app && pybabel compile -d translations

# Flaskアプリケーションがリッスンするポートを公開 (Flaskのデフォルトは5000)
EXPOSE 5000

# 環境変数（APIキーなど）を設定するためのプレースホルダー
ENV GEMINI_API_KEY=""
ENV GOOGLE_APPLICATION_CREDENTIALS=""
ENV REPLICATE_API_TOKEN=""
# 全てのAPIをスキップ（JSON生成もダミー）: デフォルトはFalse
ENV SKIP_ALL_APIS="False"
# コンテンツ生成API（画像・音声）のみスキップ: デフォルトはFalse
ENV SKIP_CONTENT_APIS="False"
# アプリケーションのパスを通す
ENV PYTHONPATH="/app"
# Flask-Babel用の環境変数
ENV BABEL_DEFAULT_LOCALE="en"
ENV BABEL_DEFAULT_TIMEZONE="UTC"

# セッション用のシークレットキー
ENV FLASK_SECRET_KEY="dev-secret-key"

# Flaskアプリケーションを実行するためのコマンド
CMD ["python", "main.py"]
