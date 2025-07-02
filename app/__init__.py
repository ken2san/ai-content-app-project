from flask import Flask
from flask_cors import CORS
import os
import logging

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for development (should be restricted in production)

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
