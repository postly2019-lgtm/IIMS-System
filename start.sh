#!/bin/bash
set -e

# Ensure we are in the right directory
cd /app

echo "Starting deployment script..."
echo "Current directory: $(pwd)"

# Run migrations
echo "🔎 Checking database readiness..."
set +e
python - <<'PY'
import os, time, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from django.db import connection
retries = int(os.environ.get('DB_READINESS_MAX_RETRIES','5'))
base = float(os.environ.get('DB_READINESS_BACKOFF_BASE','0.5'))
ready = False
last_error = None
for attempt in range(retries):
    try:
        with connection.cursor() as c:
            c.execute('SELECT 1'); c.fetchone()
        ready = True
        break
    except Exception as e:
        last_error = str(e)
        time.sleep(base * (2 ** attempt))
print('READY=' + ('1' if ready else '0'))
if not ready:
    print('DB readiness failed:', last_error)
sys.exit(0 if ready else 1)
PY
rc=$?
set -e
if [ $rc -ne 0 ]; then
  echo "❌ Database not ready. Starting in DEGRADED MODE. Skipping migrations and deploy checks."
  SKIP_DB_TASKS=1
else
  SKIP_DB_TASKS=0
fi

if [ "$SKIP_DB_TASKS" != "1" ]; then
  echo "Running migrations..."
  python manage.py migrate --no-input
fi

if [ "$SKIP_DB_TASKS" != "1" ]; then
  echo "Ensuring admin user (if ADMIN_PASSWORD is set)..."
  python manage.py ensure_admin
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Static files collection skipped"

# Start Gunicorn
echo "Starting Gunicorn on port ${PORT:-8004}..."
exec gunicorn --bind=0.0.0.0:${PORT:-8004} --timeout 600 --workers ${WEB_CONCURRENCY:-3} --log-level info --access-logfile - --error-logfile - config.wsgi:application
