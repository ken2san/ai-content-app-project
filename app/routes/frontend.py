from flask import Blueprint, render_template_string, session, request, redirect
from flask_babel import gettext as _
import os
import logging

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def serve_frontend():
    """
    Serves the frontend HTML file with translations.
    The HTML file already has _() translation tags so it can be directly rendered
    through render_template_string to apply the translations.

    If no lang parameter is provided, it may redirect to the Japanese version
    based on the DISABLE_REDIRECT_TO_JA environment variable setting.
    """
    # Check if redirects are disabled
    disable_redirect = os.getenv("DISABLE_REDIRECT_TO_JA") == "True"
    
    # Only redirect if not disabled and no language parameter is specified
    if 'lang' not in request.args and not disable_redirect:
        # Check if Accept-Language header specifies a language
        preferred = request.accept_languages.best_match(['en', 'ja'])
        if preferred != 'ja':  # If preferred language is not Japanese, redirect to Japanese
            logging.info(f"No language parameter, redirecting to /?lang=ja")
            return redirect('/?lang=ja')
        # Otherwise continue as Japanese is the default

    try:
        with open(os.path.join(os.getcwd(), 'ai_content_automation_app.html'), 'r', encoding='utf-8') as f:
            template = f.read()

        # Language switcher is already in the HTML file

        # Log the current language for debugging
        logging.info(f"Current language: {request.accept_languages.best}")

        return render_template_string(template)
    except Exception as e:
        logging.error(f"Error rendering frontend template: {str(e)}")
        return f"Error: {str(e)}", 500

@frontend_bp.route('/set-language/<lang>')
def set_language(lang):
    """
    Sets the language preference in the session.
    """
    if lang in ['en', 'ja']:
        session['lang'] = lang
    return '', 204
