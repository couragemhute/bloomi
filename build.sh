#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn --workers 3 --bind 0.0.0.0:8000 ultimate_creative.wsgi.application

