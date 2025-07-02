import datetime
import json
import os
import re
import google.generativeai as genai
from flask import request, session
from app.utils.dummy_data import get_dummy_json_prompt, DUMMY_JSON_PROMPT_EN, DUMMY_JSON_PROMPT_JA

def get_current_language():
    """
    現在の言語を取得する
    app/__init__.py の get_locale() と同じロジックで実装
    """
    # Try to get language from query parameter
    lang = request.args.get('lang')
    if lang in ['en', 'ja']:
        session['lang'] = lang  # Update session to match get_locale()
        print(f"{datetime.datetime.now()} [INFO] Language from query parameter: {lang}")
        return lang

    # Try to get language from session
    if 'lang' in session and session['lang'] in ['en', 'ja']:
        print(f"{datetime.datetime.now()} [INFO] Language from session: {session['lang']}")
        return session['lang']

    # Try to get language from Accept-Language header
    preferred = request.accept_languages.best_match(['en', 'ja'])
    if preferred:
        # 検出された言語をセッションに保存して次回使えるようにする (match get_locale())
        session['lang'] = preferred
        print(f"{datetime.datetime.now()} [INFO] Language from Accept-Language header: {preferred}")
        return preferred

    # 日本語をデフォルトに設定 (インターフェースが日本語なため)
    print(f"{datetime.datetime.now()} [INFO] No language preference detected, using Japanese (ja) as default")
    return 'ja'

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
        return get_dummy_json_prompt()

    # 現在の言語を取得
    current_lang = get_current_language()
    print(f"{datetime.datetime.now()} [INFO] Current language: {current_lang}")

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
                "title": {"type": "STRING", "description": "Title of the content"},
                "genre": {"type": "STRING", "description": "Genre of the content (e.g., Romance Drama, SF Action)"},
                "plot_summary": {"type": "STRING", "description": "Summary of the whole content"},
                "overall_mood": {"type": "STRING", "description": "Overall mood of the content (e.g., warm, thrilling)"},
                "scenes": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "scene_number": {"type": "NUMBER", "description": "Scene number"},
                            "location": {"type": "STRING", "description": "Location of the scene"},
                            "time_of_day": {"type": "STRING", "description": "Time of day in the scene"},
                            "action_description": {"type": "STRING", "description": "Description of actions and situation in the scene"},
                            "visual_style": {"type": "STRING", "description": "Visual style (e.g., anime style, live action style, nostalgic)"},
                            "dialogue": {"type": "STRING", "description": "Dialogue in the scene"},
                            "music_mood": {"type": "STRING", "description": "Mood of music for the scene"},
                            "sound_effects": {"type": "STRING", "description": "Sound effects for the scene"}
                        },
                        "required": ["scene_number", "location", "action_description", "visual_style", "dialogue", "music_mood", "sound_effects"]
                    },
                    "description": "Details of each scene composing the content"
                }
            },
            "required": ["title", "genre", "plot_summary", "overall_mood", "scenes"]
        }

        # サンプルとしてダミーデータをJSON文字列に変換
        example_json = DUMMY_JSON_PROMPT_EN if current_lang == 'en' else DUMMY_JSON_PROMPT_JA
        example_json_str = json.dumps(example_json, indent=2, ensure_ascii=False)

        print(f"{datetime.datetime.now()} [INFO] Sending request to Gemini API...")

        # 言語に応じた指示を準備
        if current_lang == 'en':
            instruction = (
                f"You are a professional scenario writer. Please generate a composition plan for video production based on the user's request in JSON format.\n"
                f"**[Critical Requirements]**\n"
                f"1.  **Output a pure JSON object only.** Do not include any extraneous information such as explanations, markdown (e.g., ```json), comments, search results, URLs, external links, dialogue, explanations, disclaimers, or incomplete outputs.\n"
                f"2.  **Never terminate output prematurely** and strictly follow the JSON schema provided and the output example below, **completely filling all required fields.**\n"
                f"3.  All string values in the JSON should be written in **English**. Do not include translations or romanized representations (including within parentheses).\n"
                f"4.  Follow the JSON syntax perfectly. In particular, do not include unescaped double quotes (\"), newlines (\\n), or backslashes (\\) within string values.\n"
                f"5.  The `scenes` array should include **3-5 scenes**, each with specific `action_description`, `visual_style`, `dialogue`, `music_mood`, and `sound_effects` **all** included.\n\n"
                f"**[Output Format Example]**\n"
                f"{example_json_str}\n\n"
                f"**[User Request]**\n"
                f"{user_prompt}\n\n"
            )
        else:  # ja
            instruction = (
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
            )

        # チャット履歴を構築
        chat_history = []
        chat_history.append({"role": "user", "parts": [{"text": instruction}]})

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
        # コード化されたバックスラッシュやクォートを処理
        cleaned_json_text = generated_json_text.strip()

        try:
            # JSON形式の文字列をパース
            generated_json = json.loads(cleaned_json_text)
            print(f"{datetime.datetime.now()} [INFO] Successfully parsed JSON response.")
            return generated_json
        except json.JSONDecodeError as json_err:
            print(f"{datetime.datetime.now()} [ERROR] Failed to parse JSON: {json_err}")
            print(f"{datetime.datetime.now()} [DEBUG] Problematic JSON: {cleaned_json_text}")
            raise ValueError(f"Generated response could not be parsed as JSON: {str(json_err)}")

    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR] Error in Gemini API call: {str(e)}")
        raise
