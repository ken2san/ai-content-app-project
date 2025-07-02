from flask import Flask, request, session, current_app
from flask_cors import CORS
from flask_babel import Babel
import os
import logging

def get_locale():
    # Try to get language from query parameter
    lang = request.args.get('lang')
    if lang in ['en', 'ja']:
        session['lang'] = lang
        logging.info(f"Language from query parameter: {lang}")
        return lang

    # Try to get language from session
    if 'lang' in session and session['lang'] in ['en', 'ja']:
        logging.info(f"Language from session: {session['lang']}")
        return session['lang']

    # Try to get language from Accept-Language header
    preferred = request.accept_languages.best_match(['en', 'ja'])
    if preferred:
        # 検出された言語をセッションに保存して次回使えるようにする
        session['lang'] = preferred
        logging.info(f"Language from Accept-Language header: {preferred}")
        return preferred

    # 日本語をデフォルトに設定 (インターフェースが日本語なため)
    logging.info("No language preference detected, using Japanese (ja) as default")
    return 'ja'

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for development (should be restricted in production)

    # Set secret key for session
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

    # JSONレスポンスの設定（日本語を直接出力）
    app.config['JSON_AS_ASCII'] = False
    app.json.ensure_ascii = False

    # Initialize Flask-Babel
    babel = Babel(app, locale_selector=get_locale)

    # ログ設定
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 環境変数の情報をログ出力
    app.logger.info(f"SKIP_ALL_APIS is set to {os.getenv('SKIP_ALL_APIS')}")
    app.logger.info(f"SKIP_CONTENT_APIS is set to {os.getenv('SKIP_CONTENT_APIS')}")
    app.logger.info(f"GEMINI_API_KEY is {'set' if os.getenv('GEMINI_API_KEY') else 'not set'}")

    # Import and register blueprints
    from app.routes.frontend import frontend_bp
    from app.routes.json_prompt import json_prompt_bp
    from app.routes.content import content_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(json_prompt_bp)
    app.register_blueprint(content_bp)

    app.logger.info("All blueprints registered")

    return app
