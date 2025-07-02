#!/bin/bash

echo "Setting up translation structure..."

# Create directory structure if it doesn't exist
mkdir -p app/translations/en/LC_MESSAGES
mkdir -p app/translations/ja/LC_MESSAGES

# Ensure there's only one translations directory
if [ -d "translations" ]; then
  echo "WARNING: Found translations in root directory. This should be moved to app/translations/"
  echo "Moving translation files to app/translations/..."

  # Copy English translations
  if [ -f "translations/en/LC_MESSAGES/messages.po" ]; then
    cp -f translations/en/LC_MESSAGES/messages.po app/translations/en/LC_MESSAGES/
    echo "Copied English translations"
  fi

  # Copy Japanese translations
  if [ -f "translations/ja/LC_MESSAGES/messages.po" ]; then
    cp -f translations/ja/LC_MESSAGES/messages.po app/translations/ja/LC_MESSAGES/
    echo "Copied Japanese translations"
  fi

  echo "Removing root translations directory..."
  rm -rf translations
  echo "Root translations directory has been removed"
fi

# Compile the translations
echo "Compiling translations..."
cd app
pybabel compile -d translations

echo "Translations consolidated and compiled!"
echo "Translation files are now in app/translations/ directory"
