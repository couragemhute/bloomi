#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

python manage.py runserver

echo "Build completed successfully!"
