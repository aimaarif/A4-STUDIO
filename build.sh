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
# Create a superuser if it doesn't exist (optional)
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('aimaa', 'a4studioa4@gmail.com', '4r3e2w1q')
EOF