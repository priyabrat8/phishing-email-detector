#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Build Tailwind CSS
python manage.py tailwind install --no-input
python manage.py tailwind build --no-input

# Gather Static Files for WhiteNoise
python manage.py collectstatic --no-input --clear

# Apply Database Tables to Neon
python manage.py migrate

# Fetch Phishing Feeds (OpenPhish / URLHaus)
python manage.py import_phishing_feeds