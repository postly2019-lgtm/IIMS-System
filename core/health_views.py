"""
Health Check Views for IIMS System
عرض فحص صحة نظام IIMS

Provides HTTP endpoints for monitoring system health.
"""

from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import sys
import os


def health_check(request):
    """
    Basic health check endpoint
    Returns 200 if system is healthy, 503 if not
    
    Usage: GET /health/
    """
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    is_healthy = True
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                health_status['checks']['database'] = {
                    'status': 'healthy',
                    'message': 'Database connection successful'
                }
            else:
                health_status['checks']['database'] = {
                    'status': 'unhealthy',
                    'message': 'Database query returned unexpected result'
                }
                is_healthy = False
    except Exception as e:
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}'
        }
        is_healthy = False
    
    # Check if in debug mode
    health_status['checks']['debug_mode'] = {
        'status': 'info',
        'value': settings.DEBUG
    }
    
    # Check Python version
    health_status['checks']['python_version'] = {
        'status': 'info',
        'value': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }
    
    # Overall status
    if not is_healthy:
        health_status['status'] = 'unhealthy'
        return JsonResponse(health_status, status=503)
    
    return JsonResponse(health_status, status=200)


def detailed_health_check(request):
    """
    Detailed health check endpoint with more information
    Only accessible to staff users
    
    Usage: GET /health/detailed/
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({
            'error': 'Unauthorized',
            'message': 'This endpoint requires staff authentication'
        }, status=403)
    
    health_status = {
        'status': 'healthy',
        'timestamp': None,
        'checks': {},
        'system_info': {}
    }
    
    from django.utils import timezone
    health_status['timestamp'] = timezone.now().isoformat()
    
    is_healthy = True
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            db_engine = settings.DATABASES['default']['ENGINE']
            db_name = settings.DATABASES['default'].get('NAME', 'N/A')
            
            health_status['checks']['database'] = {
                'status': 'healthy',
                'engine': db_engine,
                'name': db_name if 'sqlite' in db_engine else 'configured',
                'connection': 'successful'
            }
    except Exception as e:
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        is_healthy = False
    
    # Static files check
    static_root = settings.STATIC_ROOT
    if static_root and os.path.exists(static_root):
        file_count = sum([len(files) for r, d, files in os.walk(static_root)])
        health_status['checks']['static_files'] = {
            'status': 'healthy',
            'root': static_root,
            'file_count': file_count
        }
    else:
        health_status['checks']['static_files'] = {
            'status': 'warning',
            'message': 'Static root not found or empty'
        }
    
    # Environment variables check
    critical_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
    env_status = {}
    for var in critical_vars:
        value = os.environ.get(var)
        if var == 'SECRET_KEY':
            env_status[var] = 'configured' if value else 'missing'
        else:
            env_status[var] = value if value else 'not set'
    
    health_status['checks']['environment'] = {
        'status': 'info',
        'variables': env_status
    }
    
    # Groq AI check
    groq_key = getattr(settings, 'GROQ_API_KEY', None)
    health_status['checks']['groq_ai'] = {
        'status': 'configured' if groq_key else 'not configured',
        'model': getattr(settings, 'GROQ_MODEL', 'N/A')
    }
    
    # System info
    health_status['system_info'] = {
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'django_version': None,
        'debug_mode': settings.DEBUG,
        'language': settings.LANGUAGE_CODE,
        'timezone': settings.TIME_ZONE,
    }
    
    try:
        import django
        health_status['system_info']['django_version'] = django.get_version()
    except:
        pass
    
    # Overall status
    if not is_healthy:
        health_status['status'] = 'unhealthy'
        return JsonResponse(health_status, status=503)
    
    return JsonResponse(health_status, status=200)


def readiness_check(request):
    """
    Kubernetes-style readiness probe
    Returns 200 if ready to accept traffic
    
    Usage: GET /health/ready/
    """
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] != 1:
                return JsonResponse({
                    'ready': False,
                    'reason': 'Database not responding correctly'
                }, status=503)
        
        return JsonResponse({'ready': True}, status=200)
    except Exception as e:
        return JsonResponse({
            'ready': False,
            'reason': str(e)
        }, status=503)


def liveness_check(request):
    """
    Kubernetes-style liveness probe
    Returns 200 if application is alive
    
    Usage: GET /health/live/
    """
    return JsonResponse({'alive': True}, status=200)


def app_health(request):
    """
    Application health without requiring DB.
    Shows degraded status if DB unavailable.
    Usage: GET /health/app
    """
    degraded = False
    try:
        connection.ensure_connection()
    except Exception:
        degraded = True
    return JsonResponse({
        'app': 'ok' if not degraded else 'degraded',
        'debug': settings.DEBUG,
        'language': settings.LANGUAGE_CODE,
        'timezone': settings.TIME_ZONE,
    }, status=200 if not degraded else 503)


def db_health(request):
    """
    Database health with retries (exponential backoff).
    Usage: GET /health/db
    """
    retries = int(getattr(settings, 'DB_READINESS_MAX_RETRIES', 5))
    base = float(getattr(settings, 'DB_READINESS_BACKOFF_BASE', 0.5))
    for attempt in range(retries):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
            status = {
                'db': 'ok',
                'attempts': attempt + 1,
            }
            return JsonResponse(status, status=200)
        except Exception as e:
            import time
            delay = base * (2 ** attempt)
            time.sleep(delay)
            last_error = str(e)
    # Mask credentials in the DATABASE_URL if present
    raw_url = os.environ.get('DATABASE_URL', '')
    masked = 'missing'
    if raw_url:
        try:
            import re
            masked = re.sub(r'//[^/]*@', '//****@', raw_url)
        except Exception:
            masked = 'present'
    return JsonResponse({'db': 'unavailable', 'error': last_error, 'database_url': masked}, status=503)
