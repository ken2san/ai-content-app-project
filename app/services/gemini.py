import datetime
import json
import os
import re
import google.generativeai as genai
from app.utils.dummy_data import DUMMY_JSON_PROMPT

def generate_gemini_json(user_prompt):
    """
    Calls the Gemini API to generate JSON based on user input.
    Raises an exception if the API call fails.
    """
    print(f"{datetime.datetime.now()} [INFO] Generating JSON for prompt: {user_prompt}")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        error_message = "GEMINI_API_KEY is not set."
        print(f"{datetime.datetime.now()} [ERROR] {error_message}")
        raise ValueError(error_message)

    # スキップフラグを確認
    skip_all_apis = os.getenv("SKIP_ALL_APIS") == "True"
    if skip_all_apis:
        print(f"{datetime.datetime.now()} [INFO] SKIP_ALL_APIS is True, returning dummy JSON.")
        return DUMMY_JSON_PROMPT

    try:
        print(f"{datetime.datetime.now()} [INFO] Configuring Gemini API with key: {api_key[:4]}...{api_key[-4:]}")
        genai.configure(api_key=api_key)

        # Geminiモデルを初期化
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        print(f"{datetime.datetime.now()} [INFO] Using model: gemini-1.5-flash")

        # JSONスキーマを定義
        json_schema = {
            "type": "OBJECT",
            "properties": {
                "title": {"type": "STRING", "description": "コンテンツのタイトル"},
                "genre": {"type": "STRING", "description": "コンテンツのジャンル（例：ロマンスドラマ、SFアクション）"},
                "plot_summary": {"type": "STRING", "description": "コンテンツ全体のあらすじ"},
                "overall_mood": {"type": "STRING", "description": "コンテンツ全体の雰囲気（例：温かく、スリリング）"},
                "scenes": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "scene_number": {"type": "NUMBER", "description": "シーン番号"},
                            "location": {"type": "STRING", "description": "シーンの場所"},
                            "time_of_day": {"type": "STRING", "description": "シーンの時間帯"},
                            "action_description": {"type": "STRING", "description": "シーンでの具体的な行動や状況"},
                            "visual_style": {"type": "STRING", "description": "映像のスタイル（例：アニメ調、実写風、ノスタルジック）"},
                            "dialogue": {"type": "STRING", "description": "シーンでのセリフ"},
                            "music_mood": {"type": "STRING", "description": "シーンに合う音楽のムード"},
                            "sound_effects": {"type": "STRING", "description": "シーンに合う効果音"}
                        },
                        "required": ["scene_number", "location", "action_description", "visual_style", "dialogue", "music_mood", "sound_effects"]
                    },
                    "description": "コンテンツを構成する各シーンの詳細"
                }
            },
            "required": ["title", "genre", "plot_summary", "overall_mood", "scenes"]
        }

        # サンプルとしてダミーデータをJSON文字列に変換
        example_json_str = json.dumps(DUMMY_JSON_PROMPT, indent=2, ensure_ascii=False)

        print(f"{datetime.datetime.now()} [INFO] Sending request to Gemini API...")

        # チャット履歴を構築
        chat_history = []
        chat_history.append({"role": "user", "parts": [{"text": (
            f"あなたはプロのシナリオライターです。ユーザーの要望に基づき、動画制作用の構成案をJSON形式で生成してください。\n"
            f"**【厳守事項】**\n"
            f"1.  **純粋なJSONオブジェクトのみを出力してください。** 解説、マークダウン（例：```json）、コメント、検索結果、URL、外部リンク、会話文、説明、免責事項、不完全な出力など、**いかなる余計な情報も一切含めないでください。**\n"
            f"2.  出力は**決して途中で終了せず**、提供されたJSONスキーマと以下の出力例に厳密に従い、**全ての必須フィールドを完全に埋めてください。**\n"
            f"3.  JSON内の全ての文字列値は**日本語**で記述してください。英語の翻訳やローマ字表記（括弧内を含む）は含めないでください。\n"
            f"4.  JSONの構文を完璧に守ってください。特に、文字列値内部のエスケープされていない二重引用符（\"）、改行文字（\\n）、バックスラッシュ（\\）を含めないでください。\n"
            f"5.  `scenes`配列には**3〜5個**のシーンを必ず含め、各シーンには具体的な `action_description`, `visual_style`, `dialogue`, `music_mood`, `sound_effects` を**全て**含めてください。\n\n"
            f"**【出力形式の例】**\n"
            f"{example_json_str}\n\n"
            f"**【ユーザーの要望】**\n"
            f"{user_prompt}\n\n"
        )}]})

        # Gemini APIを呼び出し
        response = gemini_model.generate_content(
            chat_history,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": json_schema,
                "temperature": 0.2
            }
        )

        generated_json_text = response.candidates[0].content.parts[0].text
        print(f"{datetime.datetime.now()} [INFO] Received raw response from Gemini API.")
        print(f"{datetime.datetime.now()} [DEBUG] First 200 characters of response: {generated_json_text[:200]}...")

        # JSONテキストをクリーンアップ
        cleaned_json_text = generated_json_text.strip()
        cleaned_json_text = re.sub(r'```(?:json)?\s*(.*?)\s*```', r'\1', cleaned_json_text, flags=re.DOTALL)

        json_start_index = cleaned_json_text.find('{')
        json_end_index = cleaned_json_text.rfind('}')

        if json_start_index != -1 and json_end_index != -1 and json_end_index > json_start_index:
            cleaned_json_text = cleaned_json_text[json_start_index : json_end_index + 1]
        else:
            print(f"{datetime.datetime.now()} [WARNING] No valid JSON object start/end found in cleaned text.")
            raise ValueError("AIの応答から有効なJSONオブジェクトを抽出できませんでした。")

        try:
            generated_json_data = json.loads(cleaned_json_text)
            print(f"{datetime.datetime.now()} [INFO] Successfully parsed JSON response.")

            # JSONデータの検証
            if "scenes" not in generated_json_data or \
               not isinstance(generated_json_data["scenes"], list) or \
               not (3 <= len(generated_json_data["scenes"]) <= 5):
                print(f"{datetime.datetime.now()} [WARNING] Generated JSON is missing 'scenes' array, it is empty, or scene count is out of range (3-5).")
                raise ValueError("AIが不完全なJSON（scenesなしまたはシーン数が不正）を生成しました。")

            return generated_json_data
        except json.JSONDecodeError as json_e:
            print(f"{datetime.datetime.now()} [ERROR] JSON.loads failed even after cleanup. Error: {json_e.msg}")
            print(f"{datetime.datetime.now()} [ERROR] Cleaned JSON text: {cleaned_json_text}")
            raise ValueError(f"クリーンアップ後もJSON解析に失敗: {json_e.msg}")

    except Exception as e:
        error_message = f"Gemini API call failed: {e}"
        print(f"{datetime.datetime.now()} [ERROR] {error_message}")
        raise RuntimeError(error_message)
