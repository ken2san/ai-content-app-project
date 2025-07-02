from flask import Blueprint, request, jsonify
import os
import datetime
from app.services.content_generation import generate_content_pipeline

content_bp = Blueprint('content', __name__)

@content_bp.route('/generate-content', methods=['POST'])
def generate_content():
    """
    Receives JSON prompt and simulates AI service calls for content generation and integration.
    Skips API calls if SKIP_ALL_APIS=True or SKIP_CONTENT_APIS=True.
    """
    data = request.json
    if not data or 'scenes' not in data:
        return jsonify({"error": "No scenes data provided"}), 400

    try:
        result = generate_content_pipeline(data)
        return jsonify(result), 200
    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR] Content generation failed: {e}")
        return jsonify({"error": "Content generation failed."}), 500
