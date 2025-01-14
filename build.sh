#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment..."

# Activate virtual environment (adjust path as necessary)
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Apply migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn ultimate_creative.wsgi:application \
    --workers 3 \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

echo "Deployment was successful. Project is now running!"
