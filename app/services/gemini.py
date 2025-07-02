import datetime
import json
import re
from app.utils.dummy_data import DUMMY_JSON_PROMPT

# Placeholder for Gemini API configuration and call
def generate_gemini_json(user_prompt):
    """
    Simulates a call to the Gemini API to generate JSON based on user input.
    Returns dummy data if the API is not configured.
    """
    print(f"{datetime.datetime.now()} [INFO] Generating JSON for prompt: {user_prompt}")

    # Simulate API call and response
    try:
        # Replace this with actual Gemini API logic
        generated_json = DUMMY_JSON_PROMPT
        return generated_json
    except Exception as e:
        print(f"{datetime.datetime.now()} [ERROR] Gemini API call failed: {e}")
        raise
