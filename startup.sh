#!/bin/bash
# Startup script for IIMS System - Railway/Production
set -e

echo "=========================================="
echo "🚀 IIMS System - Startup Process"
echo "=========================================="

# Display environment info
echo "📋 Startup Information:"
echo "   Current Directory: $(pwd)"
echo "   Python Version: $(python --version)"
echo "   Django Version: $(python -c 'import django; print(django.get_version())')"
echo "   Port: ${PORT:-8004}"
echo "   Workers: ${WEB_CONCURRENCY:-3}"
echo ""

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
  echo "🗄️  Running database migrations..."
  python manage.py migrate --no-input
  echo "✅ Migrations completed"
  echo ""
fi

# Ensure admin user exists (if ADMIN_PASSWORD is set)
echo "👤 Checking admin user..."
if [ "$SKIP_DB_TASKS" != "1" ]; then
  if [ -n "$ADMIN_PASSWORD" ]; then
      python manage.py ensure_admin
      echo "✅ Admin user configured"
  else
      echo "ℹ️  ADMIN_PASSWORD not set, skipping admin creation"
  fi
  echo ""
fi

# Collect static files (in case they weren't collected during build)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Static files collection skipped"
echo ""

# Health check before starting
if [ "$SKIP_DB_TASKS" != "1" ]; then
  echo "🏥 Running health checks..."
  python manage.py check --deploy || echo "⚠️  Some deployment checks failed (non-critical)"
  echo ""
else
  echo "🏥 Skipping deployment checks due to DB unavailability"
fi

# Calculate optimal workers
WORKERS=${WEB_CONCURRENCY:-3}
echo "=========================================="
echo "🌐 Starting Gunicorn Server"
   echo "   Binding: 0.0.0.0:${PORT:-8004}"
   echo "   Workers: $WORKERS"
   echo "   Timeout: 600s"
   echo "   Log Level: info"
echo "=========================================="
echo ""

# Start Gunicorn with optimized settings (works in both normal and degraded modes)
exec gunicorn \
    --bind=0.0.0.0:${PORT:-8004} \
    --workers=$WORKERS \
    --timeout=600 \
    --worker-class=sync \
    --worker-tmp-dir=/dev/shm \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=- \
    --capture-output \
    --enable-stdio-inheritance \
    config.wsgi:application
