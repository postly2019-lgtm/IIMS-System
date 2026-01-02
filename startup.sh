#!/bin/bash
set -e
echo "Starting deployment script..."
echo "Current directory: $(pwd)"
echo "Environment variables check:"
echo "GROQ_API_KEY: ${GROQ_API_KEY:+SET (hidden)} ${GROQ_API_KEY:-NOT SET}"
echo "DATABASE_URL: ${DATABASE_URL:+SET ($DATABASE_URL)} ${DATABASE_URL:-NOT SET (using default SQLite)}"
echo "DEBUG: $DEBUG"
echo "SECRET_KEY: ${SECRET_KEY:+SET} ${SECRET_KEY:-NOT SET}"
echo "PORT: $PORT"

echo "Running migrations..."
python manage.py migrate || { echo "Migration failed"; exit 1; }

echo "Ensuring admin user (if ADMIN_PASSWORD is set)..."
python manage.py init_sec_user || echo "init_sec_user failed, continuing..."

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || { echo "Collectstatic failed"; exit 1; }

echo "Testing Django setup..."
python manage.py check --deploy || { echo "Django check failed"; exit 1; }

echo "Starting Gunicorn on port ${PORT:-8004}..."
exec gunicorn --bind=0.0.0.0:${PORT:-8004} --timeout 600 --workers 3 --log-level debug --access-logfile - --error-logfile - config.wsgi:application
