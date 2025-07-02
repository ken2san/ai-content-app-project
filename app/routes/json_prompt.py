from flask import Blueprint, request, jsonify, current_app
from flask_babel import gettext as _
import datetime
import json
import os
from app.services.gemini import generate_gemini_json
from app.utils.dummy_data import get_dummy_json_prompt

json_prompt_bp = Blueprint('json_prompt', __name__)

# カスタムJSONエンコーダー（日本語を直接出力）
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return json.JSONEncoder.default(self, obj)

@json_prompt_bp.route('/generate-json-prompt', methods=['POST'])
def generate_json_prompt():
    """
    Endpoint for AI to generate a JSON prompt based on user input.
    Returns dummy data if SKIP_ALL_APIS is True or if AI generation fails.
    """
    # ensure_ascii=Falseを使用するためにカスタムJSONエンコーダーを設定
    current_app.json.ensure_ascii = False
    print(f"{datetime.datetime.now()} [INFO] Received request to /generate-json-prompt")

    # リクエストデータを検証
    request_data = request.get_json()
    if not request_data:
        print(f"{datetime.datetime.now()} [ERROR] No JSON data in request")
        return jsonify({"error": _("リクエストにJSONデータが含まれていません")}), 400

    user_prompt = request_data.get('userPrompt')
    if not user_prompt:
        print(f"{datetime.datetime.now()} [ERROR] No userPrompt in request: {request_data}")
        return jsonify({"error": _("ユーザープロンプトが提供されていません")}), 400

    print(f"{datetime.datetime.now()} [INFO] Processing prompt: {user_prompt[:50]}...")

    # SKIP_ALL_APISフラグを確認
    skip_all_apis = os.getenv("SKIP_ALL_APIS") == "True"
    if skip_all_apis:
        print(f"{datetime.datetime.now()} [INFO] SKIP_ALL_APIS is True, returning dummy JSON prompt.")
        return jsonify({
            "json_data": get_dummy_json_prompt(),
            "message": _("APIスキップのためダミーJSONを生成しました。")
        }), 200

    try:
        print(f"{datetime.datetime.now()} [INFO] Calling generate_gemini_json")
        generated_json = generate_gemini_json(user_prompt)
        print(f"{datetime.datetime.now()} [INFO] Successfully generated JSON")
        return jsonify({
            "json_data": generated_json,
            "message": _("JSONプロンプト生成完了！")
        }), 200
    except ValueError as ve:
        print(f"{datetime.datetime.now()} [ERROR] Value error in JSON generation: {ve}")
        return jsonify({
            "error": _("JSON生成中にエラーが発生しました: {error}").format(error=str(ve)),
            "dummy_fallback": True,
            "json_data": get_dummy_json_prompt()
        }), 500
    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR] Unexpected error in JSON generation: {e}")
        return jsonify({
            "error": _("JSON生成中にエラーが発生しました。ダミーデータを使用します。詳細: {error}").format(error=str(e)),
            "dummy_fallback": True,
            "json_data": get_dummy_json_prompt()
        }), 500
