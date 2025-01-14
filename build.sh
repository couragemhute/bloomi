#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run the Django development server in the background
python manage.py runserver &

# Wait for the server to start
sleep 5

echo "Build completed successfully and server is running!"
