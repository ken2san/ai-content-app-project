# AI Content Automation App with Multilingual Support

A Flask-based AI content generation app with modular architecture, Docker support, and multilingual capabilities using Flask-Babel.

## Features

- Language switching between English and Japanese
- AI content generation and processing
- Docker containerization for easy deployment

## Language Switching Implementation

The application uses Flask-Babel for internationalization (i18n) and localization (l10n). Here's how it works:

1. **Language Detection**:

   - URL parameter: `/?lang=en` or `/?lang=ja`
   - Session storage: Once selected, language preference is stored in the session
   - Browser preference: Falls back to the browser's Accept-Language header
   - Default: English (`en`)

2. **Translation Files**:

   - Located in `app/translations/`
   - English: `app/translations/en/LC_MESSAGES/messages.po`
   - Japanese: `app/translations/ja/LC_MESSAGES/messages.po`
   - Compiled to `.mo` files during Docker build

3. **Translation Tags**:
   - HTML templates use Flask-Babel's `{{ _('text to translate') }}` syntax
   - Python code uses `gettext` function imported as `_`

## Development Workflow

### Environment Variables

The following environment variables can be set in docker-compose.yml:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `SKIP_CONTENT_APIS`: Set to "True" to use dummy data instead of actual API calls
- `DISABLE_REDIRECT_TO_JA`: Set to "True" to disable automatic redirects to Japanese locale (useful for testing)

### Updating Translations

1. Extract translatable strings:

   ```bash
   pybabel extract -F babel.cfg -o app/translations/messages.pot .
   ```

2. Update existing translation files:

   ```bash
   pybabel update -i app/translations/messages.pot -d app/translations
   ```

3. Edit the `.po` files in `app/translations/[lang]/LC_MESSAGES/`

4. Compile translations:

   ```bash
   pybabel compile -d app/translations
   ```

5. Alternatively, use the provided script:
   ```bash
   ./update_translations.sh
   ```

### Running and Testing

1. Run the comprehensive test and launch script:

   ```bash
   ./test_app.sh
   ```

   This script:

   - Checks translation file structure
   - Builds and starts the Docker container
   - Tests UI language switching
   - Tests JSON API language support
   - Provides helpful commands and URLs

2. Access the application:

   - English: http://localhost:8000/?lang=en
   - Japanese: http://localhost:8000/?lang=ja

3. Clean up redundant files (after confirming functionality):

   ```bash
   ./cleanup.sh
   ```

## Project Structure

```
.
├── app/
│   ├── __init__.py           # App initialization with Babel setup
│   ├── routes/               # Application routes
│   ├── services/             # Service modules
│   ├── translations/         # Translation files (ONLY valid location)
│   │   ├── en/
│   │   │   └── LC_MESSAGES/
│   │   │       └── messages.po
│   │   └── ja/
│   │       └── LC_MESSAGES/
│   │           └── messages.po
│   └── utils/                # Utility functions
├── ai_content_automation_app.html  # Main HTML template with translation tags
├── app.py                    # Application entry point
├── babel.cfg                 # Babel configuration
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker build configuration
├── fix_translations.sh       # Script to fix translation file issues
├── main.py                   # Docker entry point
├── requirements.txt          # Python dependencies
├── test_app.sh              # Comprehensive testing and launch script
├── cleanup.sh               # Script to remove redundant files
├── TRANSLATIONS.md           # Translation workflow documentation
└── update_translations.sh    # Script to update translations
```

## Requirements

- Docker and Docker Compose
- Flask-Babel (included in requirements.txt)
- Python 3.9+
