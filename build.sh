#!/usr/bin/env bash
# Exit on error
set -o errexit

# Create a log file
LOG_FILE="deploy.log"
echo "Deployment started at $(date)" > $LOG_FILE

# Log function to capture command output and errors
log_and_run() {
  echo "Running: $1" | tee -a $LOG_FILE
  eval $1 >> $LOG_FILE 2>&1
  if [ $? -ne 0 ]; then
    echo "Error: Command failed - $1" | tee -a $LOG_FILE
    exit 1
  fi
}

# Install dependencies
log_and_run "pip install -r requirements.txt"

# Collect static files
log_and_run "python manage.py collectstatic --no-input"

# Apply database migrations
log_and_run "python manage.py migrate"

# Final log message
echo "Deployment completed successfully at $(date)" | tee -a $LOG_FILE
