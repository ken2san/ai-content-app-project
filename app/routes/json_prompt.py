from flask import Blueprint, request, jsonify
import datetime
import json
import os
from app.services.gemini import generate_gemini_json
from app.utils.dummy_data import DUMMY_JSON_PROMPT

json_prompt_bp = Blueprint('json_prompt', __name__)

@json_prompt_bp.route('/generate-json-prompt', methods=['POST'])
def generate_json_prompt():
    """
    Endpoint for AI to generate a JSON prompt based on user input.
    Returns dummy data if SKIP_ALL_APIS is True or if AI generation fails.
    """
    print(f"{datetime.datetime.now()} [INFO] Received request to /generate-json-prompt")

    # リクエストデータを検証
    request_data = request.get_json()
    if not request_data:
        print(f"{datetime.datetime.now()} [ERROR] No JSON data in request")
        return jsonify({"error": "リクエストにJSONデータが含まれていません"}), 400

    user_prompt = request_data.get('userPrompt')
    if not user_prompt:
        print(f"{datetime.datetime.now()} [ERROR] No userPrompt in request: {request_data}")
        return jsonify({"error": "ユーザープロンプトが提供されていません"}), 400

    print(f"{datetime.datetime.now()} [INFO] Processing prompt: {user_prompt[:50]}...")

    # SKIP_ALL_APISフラグを確認
    skip_all_apis = os.getenv("SKIP_ALL_APIS") == "True"
    if skip_all_apis:
        print(f"{datetime.datetime.now()} [INFO] SKIP_ALL_APIS is True, returning dummy JSON prompt.")
        return jsonify({
            "json_data": DUMMY_JSON_PROMPT,
            "message": "APIスキップのためダミーJSONを生成しました。"
        }), 200

    try:
        print(f"{datetime.datetime.now()} [INFO] Calling generate_gemini_json")
        generated_json = generate_gemini_json(user_prompt)
        print(f"{datetime.datetime.now()} [INFO] Successfully generated JSON")
        return jsonify({
            "json_data": generated_json,
            "message": "JSONプロンプト生成完了！"
        }), 200
    except ValueError as ve:
        print(f"{datetime.datetime.now()} [ERROR] Value error in JSON generation: {ve}")
        return jsonify({
            "error": f"JSON生成中にエラーが発生しました: {str(ve)}",
            "dummy_fallback": True,
            "json_data": DUMMY_JSON_PROMPT
        }), 500
    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR] Unexpected error in JSON generation: {e}")
        return jsonify({
            "error": f"JSON生成中にエラーが発生しました。ダミーデータを使用します。詳細: {str(e)}",
            "dummy_fallback": True,
            "json_data": DUMMY_JSON_PROMPT
        }), 500
