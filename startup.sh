#!/bin/bash
set -e
echo "Starting deployment script..."
echo "Current directory: $(pwd)"
echo "Listing directory contents:"
ls -la

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn --bind=0.0.0.0:${PORT:-8000} --timeout 600 --workers 3 --log-level debug --access-logfile - --error-logfile - config.wsgi
