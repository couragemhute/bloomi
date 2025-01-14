
#!/bin/bash
SECRET_KEY=$(openssl rand -base64 32)  # Generate a random secret key
WEB_CONCURRENCY=4
PROJECT_NAME="ultimate_creative"
RUNTIME="python"
START_COMMAND="gunicorn ultimate_creative.asgi:application -k uvicorn.workers.UvicornWorker --workers $WEB_CONCURRENCY"

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment for project: $PROJECT_NAME"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Environment Variables Setup
echo "Configuring environment variables..."
export DATABASE_URL=$DATABASE_URL
export SECRET_KEY=$SECRET_KEY
export WEB_CONCURRENCY=$WEB_CONCURRENCY

# Start the web server
echo "Starting the application using: $START_COMMAND"
eval $START_COMMAND

echo "Deployment was successful. $PROJECT_NAME is now running!"
