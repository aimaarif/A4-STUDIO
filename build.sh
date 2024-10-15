#!/usr/bin/env bash

# Exit immediately if any command exits with a non-zero status
set -o errexit

# Install Python dependencies
pip install --upgrade pip  # Make sure pip is up to date
pip install -r requirements.txt  # Install all dependencies listed in requirements.txt

# Apply database migrations
python manage.py migrate  # Run migrations to set up or update the database schema

# Collect static files
python manage.py collectstatic --noinput  # Collect static files for production use

# (Optional) You may want to run tests here to ensure the build is working
# python manage.py test

# Run other custom commands if needed
