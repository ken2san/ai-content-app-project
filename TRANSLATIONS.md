# Translation Quick Reference Guide

This document provides a quick reference for working with translations in this project.

## Adding Translatable Strings

### In HTML Templates

Use the following syntax in HTML templates:

```html
<!-- Basic text -->
<h1>{{ _('Hello World') }}</h1>

<!-- With variables -->
<p>{{ _('Welcome, %(name)s', name=user.name) }}</p>

<!-- Pluralization -->
<p>{{ ngettext('%(num)d file', '%(num)d files', files|length) }}</p>
```

### In Python Code

```python
from flask_babel import gettext as _

# Basic text
message = _('Hello World')

# With variables
message = _('Welcome, %(name)s', name=user.name)

# Pluralization
from flask_babel import ngettext
message = ngettext('%(num)d file', '%(num)d files', len(files))
```

## Translation Workflow

1. **Add translations tags** to your HTML and Python code using `{{ _('text') }}` in templates or `_('text')` in Python code.

2. **Extract messages** to the POT file:

   ```bash
   pybabel extract -F babel.cfg -o app/translations/messages.pot .
   ```

3. **Initialize a new language** (if needed):

   ```bash
   pybabel init -i app/translations/messages.pot -d app/translations -l [LANGUAGE_CODE]
   ```

   Example: `pybabel init -i app/translations/messages.pot -d app/translations -l fr`

4. **Update existing translations**:

   ```bash
   pybabel update -i app/translations/messages.pot -d app/translations
   ```

5. **Edit the PO files** found in `app/translations/[LANGUAGE_CODE]/LC_MESSAGES/messages.po`

   - Fill in the missing translations or update existing ones

6. **Compile translations**:

   ```bash
   pybabel compile -d app/translations
   ```

7. **Restart the application** to see the changes.

## 重要な注意事項

翻訳ファイルは必ず `app/translations/` ディレクトリ内に置いてください。ルートディレクトリの `translations/` は使用しないでください。

## Using The Helper Scripts

1. **Update all translations** using:

   ```bash
   ./update_translations.sh
   ```

2. **Fix translation directory issues**:

   ```bash
   ./fix_translations.sh
   ```

3. **Test language switching**:
   ```bash
   ./test_language_switching.sh
   ```

## Language URL Parameters

- English: `/?lang=en`
- Japanese: `/?lang=ja`
- To add a new language, update the `get_locale` function in `app/__init__.py`
