from flask import Blueprint, request, jsonify
import datetime
import json
from app.services.gemini import generate_gemini_json

json_prompt_bp = Blueprint('json_prompt', __name__)

@json_prompt_bp.route('/generate-json-prompt', methods=['POST'])
def generate_json_prompt():
    """
    Endpoint for AI to generate a JSON prompt based on user input.
    Returns dummy data if SKIP_ALL_APIS is True or if AI generation fails.
    """
    user_prompt = request.json.get('userPrompt')
    if not user_prompt:
        return jsonify({"error": "ユーザープロンプトが提供されていません"}), 400

    try:
        generated_json = generate_gemini_json(user_prompt)
        return jsonify({"json_data": generated_json, "message": "JSONプロンプト生成完了！"}), 200
    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR] JSON generation failed: {e}")
        return jsonify({"error": "JSON生成中にエラーが発生しました。"}), 500
