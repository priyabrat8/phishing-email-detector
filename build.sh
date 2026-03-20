#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Build Tailwind CSS (Removed the flags here)
python manage.py tailwind install
python manage.py tailwind build

# Gather Static Files for WhiteNoise (Keep the flags here!)
python manage.py collectstatic --no-input --clear

# Apply Database Tables to Neon
python manage.py migrate

# Fetch Phishing Feeds (OpenPhish / URLHaus)
python manage.py import_phishing_feeds