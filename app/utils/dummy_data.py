from flask import request, session

# 英語版のダミーデータ
DUMMY_JSON_PROMPT_EN = {
    "title": "Childhood Friends: A Test Story",
    "genre": "Human Drama, Heartwarming",
    "plot_summary": "A touching story of two people who grew up together, overcoming various aspects of life and bonded by a deep connection.",
    "overall_mood": "Warm",
    "scenes": [
        {
            "scene_number": 1,
            "location": "Memory Park",
            "time_of_day": "Sunny Afternoon",
            "action_description": "Two young children laughing together on swings. The beginning of friendship.",
            "visual_style": "Bright, nostalgic anime style",
            "dialogue": "(Boy) \"We'll be friends forever!\"\n(Girl) \"Yes!\"",
            "music_mood": "Innocent",
            "sound_effects": "Birds chirping"
        },
        {
            "scene_number": 2,
            "location": "High School Graduation",
            "time_of_day": "Dusk",
            "action_description": "Looking at each other with diplomas in hand, filled with hope for the future and a bit of anxiety.",
            "visual_style": "Youthful radiance",
            "dialogue": "(He) \"I never thought we'd make it this far...\"\n(She) \"Here's to the future, together.\"",
            "music_mood": "Melancholic",
            "sound_effects": "Sound of wind"
        },
        {
            "scene_number": 3,
            "location": "Honeymoon Beach",
            "time_of_day": "Beautiful Sunset",
            "action_description": "The two hold hands and walk along the shore. Feeling ultimate happiness.",
            "visual_style": "Romantic",
            "dialogue": "(Husband) \"It's like a dream.\"\n(Wife) \"It's not a dream.\"",
            "music_mood": "Blissful",
            "sound_effects": "Sounds of waves"
        }
    ]
}

# 日本語版のダミーデータ
DUMMY_JSON_PROMPT_JA = {
    "title": "幼馴染の絆：テスト物語",
    "genre": "ヒューマンドラマ、感動",
    "plot_summary": "幼い頃から共に育った二人が、人生の様々な局面を乗り越え、深い絆で結ばれる感動の物語。",
    "overall_mood": "温かく",
    "scenes": [
        {
            "scene_number": 1,
            "location": "思い出の公園",
            "time_of_day": "晴れた午後",
            "action_description": "幼い二人がブランコで笑い合う。友情の始まり。",
            "visual_style": "明るく、ノスタルジックなアニメ調",
            "dialogue": "（少年）「ずっと友達だよ！」\n（少女）「うん！」",
            "music_mood": "無邪気",
            "sound_effects": "鳥のさえずり"
        },
        {
            "scene_number": 2,
            "location": "高校の卒業式",
            "time_of_day": "夕暮れ",
            "action_description": "卒業証書を手に、未来への希望と少しの不安を抱えながら、お互いを見つめ合う。",
            "visual_style": "青春の輝き",
            "dialogue": "（彼）「まさか、ここまで来るとはな…」\n（彼女）「これからも、よろしくね。」",
            "music_mood": "切なさ",
            "sound_effects": "風の音"
        },
        {
            "scene_number": 3,
            "location": "新婚旅行先のビーチ",
            "time_of_day": "美しい夕日",
            "action_description": "二人が手を取り合い、波打ち際を歩く。最高の幸せを感じる瞬間。",
            "visual_style": "ロマンチック",
            "dialogue": "（夫）「夢みたいだ。」\n（妻）「夢じゃないよ。」",
            "music_mood": "幸福感",
            "sound_effects": "波の音"
        }
    ]
}

# 古い変数名との互換性のために、ダミーのJSONプロンプトをデフォルトの日本語バージョンにマッピング
DUMMY_JSON_PROMPT = DUMMY_JSON_PROMPT_JA

def get_dummy_json_prompt():
    """
    現在の言語に基づいてダミーのJSONプロンプトを取得
    """
    # Try to get language from query parameter or session
    lang = request.args.get('lang')
    if not lang and 'lang' in session:
        lang = session.get('lang')

    # If lang is English, return English dummy data
    if lang == 'en':
        return DUMMY_JSON_PROMPT_EN

    # Default to Japanese
    return DUMMY_JSON_PROMPT_JA
