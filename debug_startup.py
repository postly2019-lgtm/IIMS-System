import sys
import os
import django
from django.conf import settings

print("--- DEBUG STARTUP ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"PORT Environment Variable: {os.environ.get('PORT')}")

# Check if settings can be configured
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    print("Django setup successful.")
except Exception as e:
    print(f"CRITICAL: Django setup failed: {e}")
    sys.exit(1)

# Check database connection
from django.db import connections
from django.db.utils import OperationalError
try:
    conn = connections['default']
    print(f"Database Engine: {conn.settings_dict['ENGINE']}")
    # conn.cursor() # This might fail if DB is not ready, but we want to know
    print("Database configuration seems valid.")
except Exception as e:
    print(f"WARNING: Database check failed (might be unreachable): {e}")

# Check WSGI import
try:
    import config.wsgi
    print("WSGI module imported successfully.")
except Exception as e:
    print(f"CRITICAL: WSGI import failed: {e}")
    sys.exit(1)

print("--- DEBUG COMPLETE ---")
