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

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input
echo "✅ Migrations completed"
echo ""

# Ensure admin user exists (if ADMIN_PASSWORD is set)
echo "👤 Checking admin user..."
if [ -n "$ADMIN_PASSWORD" ]; then
    python manage.py ensure_admin
    echo "✅ Admin user configured"
else
    echo "ℹ️  ADMIN_PASSWORD not set, skipping admin creation"
fi
echo ""

# Collect static files (in case they weren't collected during build)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Static files collection skipped"
echo ""

# Health check before starting
echo "🏥 Running health checks..."
python manage.py check --deploy || echo "⚠️  Some deployment checks failed (non-critical)"
echo ""

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

# Start Gunicorn with optimized settings
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
