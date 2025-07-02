#!/bin/bash

# Script to extract translatable strings and update translation files

set -e

# Ensure correct directory structure exists
mkdir -p app/translations/en/LC_MESSAGES
mkdir -p app/translations/ja/LC_MESSAGES

echo "Extracting translatable strings from templates and Python files..."
# Extract messages from Python files and HTML templates
pybabel extract -F babel.cfg -o app/translations/messages.pot .

echo "Updating translation files..."
# Update existing translation files
pybabel update -i app/translations/messages.pot -d app/translations

echo "Compiling translation files..."
# Compile translation files to .mo format
pybabel compile -d app/translations

echo "✅ Translation files updated and compiled successfully!"
echo "You can edit the .po files in app/translations/[lang]/LC_MESSAGES/ for further translation updates."
