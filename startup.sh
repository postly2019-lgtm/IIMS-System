#!/bin/bash
echo "Starting deployment script..."
echo "Running migrations..."
python manage.py migrate
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Starting Gunicorn on port ${PORT:-8000}..."
gunicorn --bind=0.0.0.0:${PORT:-8000} --timeout 600 --access-logfile - --error-logfile - config.wsgi
