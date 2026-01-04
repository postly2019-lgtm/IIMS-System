import time
import logging
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.db import connection
from django.utils.deprecation import MiddlewareMixin


DB_READINESS_MAX_RETRIES = int(getattr(settings, 'DB_READINESS_MAX_RETRIES', 5))
DB_READINESS_BACKOFF_BASE = float(getattr(settings, 'DB_READINESS_BACKOFF_BASE', 0.5))

WHITELIST_PREFIXES = (
    '/health',
    getattr(settings, 'STATIC_URL', '/static/'),
    '/favicon.ico',
)


class RequestIDFilter(logging.Filter):
    """
    Logging filter to attach request ID to log records.
    If no request ID is available, uses 'no-request-id'.
    """
    def filter(self, record):
        record.request_id = getattr(record, 'request_id', 'no-request-id')
        return True


class RequestIDMiddleware(MiddlewareMixin):
    """
    Middleware to generate and attach a unique request ID to each request.
    The request ID is used for log correlation and debugging.
    """
    def process_request(self, request):
        # Generate a unique request ID
        request.request_id = str(uuid.uuid4())
        return None

    def process_response(self, request, response):
        # Add request ID to response headers for debugging
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = request.request_id
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log incoming requests and outgoing responses.
    Logs include request ID, method, path, user, and response time.
    """
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = logging.getLogger('iims.requests')

    def process_request(self, request):
        # Store request start time
        request._start_time = time.time()
        return None

    def process_response(self, request, response):
        # Skip logging for health checks and static files
        if any(request.path.startswith(pfx) for pfx in WHITELIST_PREFIXES):
            return response
        
        # Calculate request duration
        duration = 0
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
        
        # Get request ID
        request_id = getattr(request, 'request_id', 'unknown')
        
        # Get user info
        user_info = 'Anonymous'
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_info = f"{request.user.username} (ID: {request.user.id})"
        
        # Create log record with request ID
        log_record = self.logger.makeRecord(
            self.logger.name, logging.INFO, '', 0, 
            f"{request.method} {request.path} - Status: {response.status_code} - "
            f"User: {user_info} - Duration: {duration:.3f}s",
            (), None
        )
        log_record.request_id = request_id
        self.logger.handle(log_record)
        
        return response

    def process_exception(self, request, exception):
        # Log exceptions with request ID
        request_id = getattr(request, 'request_id', 'unknown')
        
        log_record = self.logger.makeRecord(
            self.logger.name, logging.ERROR, '', 0,
            f"Exception during {request.method} {request.path}: {str(exception)}",
            (), None
        )
        log_record.request_id = request_id
        self.logger.handle(log_record)
        
        return None


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
