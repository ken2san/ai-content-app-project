from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for development (should be restricted in production)

    # Import and register blueprints
    from app.routes.frontend import frontend_bp
    from app.routes.json_prompt import json_prompt_bp
    from app.routes.content import content_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(json_prompt_bp)
    app.register_blueprint(content_bp)

    return app
