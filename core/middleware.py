import time
import logging
from django.conf import settings
from django.http import JsonResponse
from django.db import connection


DB_READINESS_MAX_RETRIES = int(getattr(settings, 'DB_READINESS_MAX_RETRIES', 5))
DB_READINESS_BACKOFF_BASE = float(getattr(settings, 'DB_READINESS_BACKOFF_BASE', 0.5))

WHITELIST_PREFIXES = (
    '/health',
    getattr(settings, 'STATIC_URL', '/static/'),
    '/favicon.ico',
)


def _check_db_ready(retries: int = DB_READINESS_MAX_RETRIES, base_delay: float = DB_READINESS_BACKOFF_BASE) -> bool:
    logger = logging.getLogger('iims.db')
    for attempt in range(retries):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
            if attempt > 0:
                logger.info(f"DB readiness confirmed after {attempt+1} attempts")
            return True
        except Exception as e:
            delay = base_delay * (2 ** attempt)
            logger.warning(f"DB not ready (attempt {attempt+1}/{retries}): {e}. Retrying in {delay:.2f}s")
            time.sleep(delay)
    logger.error("DB readiness failed after maximum retries")
    return False


class DBReadinessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('iims.db')

    def __call__(self, request):
        if getattr(settings, 'IS_TESTING', False) or settings.DEBUG:
            return self.get_response(request)

        path = request.path
        if any(path.startswith(pfx) for pfx in WHITELIST_PREFIXES):
            return self.get_response(request)

        if not _check_db_ready():
            return JsonResponse({
                'status': 'degraded',
                'message': 'النظام يعمل بوضع التدهور لعدم توفر قاعدة البيانات',
                'allowlist': list(WHITELIST_PREFIXES),
            }, status=503)

        return self.get_response(request)
