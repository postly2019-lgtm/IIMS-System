#!/bin/bash
set -e

# Ensure we are in the right directory
cd /app

echo "Starting deployment script..."
echo "Current directory: $(pwd)"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "Starting Gunicorn on port ${PORT:-8004}..."
exec gunicorn --bind=0.0.0.0:${PORT:-8004} --timeout 600 --workers 3 --log-level debug --access-logfile - --error-logfile - config.wsgi:application
