from flask import Blueprint, send_from_directory
import os

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def serve_frontend():
    """
    Serves the frontend HTML file.
    """
    return send_from_directory(os.getcwd(), 'ai_content_automation_app.html')
