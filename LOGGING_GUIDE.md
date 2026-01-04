# IIMS System - Logging and Debugging Guide

This guide explains the logging and debugging infrastructure implemented in the IIMS System.

## Overview

The IIMS System uses a comprehensive logging configuration that provides:
- **Request tracking** with unique request IDs
- **Multiple log levels** for different environments
- **Rotating log files** to prevent disk space issues
- **Structured logging** with consistent formatting
- **Module-specific loggers** for better organization

## Logging Configuration

### Log Levels

The system uses different log levels based on the environment:

| Environment | Level | Description |
|-------------|-------|-------------|
| Development (DEBUG=True) | DEBUG | All log messages including debug info |
| Production (DEBUG=False) | INFO | Information, warnings, and errors only |

### Log Files

All log files are stored in the `logs/` directory (automatically created):

| File | Purpose | Max Size | Backups |
|------|---------|----------|---------|
| `iims.log` | General application logs | 10 MB | 5 |
| `iims_errors.log` | Error logs only | 10 MB | 5 |
| `iims_db.log` | Database-related logs | 5 MB | 3 |

Logs automatically rotate when they reach the maximum size, keeping the specified number of backup files.

### Log Format

Logs include the following information:

```
[LEVEL] timestamp [request-id] logger_name function:line - message
```

Example:
```
[INFO] 2026-01-04 10:30:15 [a1b2c3d4-e5f6-7890-abcd-ef1234567890] core login_view:45 - User admin successfully logged in from IP 192.168.1.1
```

## Request ID Tracking

### What is a Request ID?

Every HTTP request to the IIMS system automatically receives a unique identifier (UUID) that:
- Appears in all log messages related to that request
- Is included in the response headers (`X-Request-ID`)
- Helps trace the complete lifecycle of a request

### How to Use Request IDs

When investigating an issue:

1. **Find the Request ID** from error messages, user reports, or HTTP response headers
2. **Search logs** for that specific request ID:
   ```bash
   grep "a1b2c3d4-e5f6-7890-abcd-ef1234567890" logs/iims.log
   ```
3. **Trace the request** through all log entries to understand the flow

### Example Request Trace

```
[INFO] 2026-01-04 10:30:15 [abc-123] iims.requests - GET /intel/dashboard/ - Status: 200 - User: admin (ID: 1) - Duration: 0.145s
[INFO] 2026-01-04 10:30:15 [abc-123] core - User admin successfully logged in from IP 192.168.1.1
[INFO] 2026-01-04 10:30:16 [abc-123] intelligence - Translation requested for report 42 by user admin
```

## Using Loggers in Code

### Core and Intelligence Apps

The core and intelligence apps have pre-configured loggers:

```python
import logging

# Get the logger for your module
logger = logging.getLogger('core')  # or 'intelligence', 'intelligence_agent'

# Log with request context
def _log_with_request(request, level, message):
    """Helper to log with request ID context"""
    log_record = logger.makeRecord(
        logger.name, level, '', 0, message, (), None
    )
    log_record.request_id = getattr(request, 'request_id', 'no-request-id')
    logger.handle(log_record)

# In your view
def my_view(request):
    _log_with_request(
        request, logging.INFO,
        f"Processing action for user {request.user.username}"
    )
```

### Standard Logging (without request context)

For background tasks or non-request contexts:

```python
import logging

logger = logging.getLogger('intelligence.ingestion')

# Simple logging
logger.info("Starting RSS ingestion")
logger.warning("Feed parsing failed for source XYZ")
logger.error(f"Exception occurred: {str(e)}")
```

### Log Level Guidelines

- **DEBUG**: Detailed diagnostic information (disabled in production)
  ```python
  logger.debug(f"Processing entry: {entry}")
  ```

- **INFO**: Informational messages about normal operations
  ```python
  logger.info(f"User {username} logged in successfully")
  ```

- **WARNING**: Warning messages about potential issues
  ```python
  logger.warning(f"Failed login attempt for username '{username}'")
  ```

- **ERROR**: Error messages for handled exceptions
  ```python
  logger.error(f"Translation failed: {str(e)}")
  ```

- **CRITICAL**: Critical system errors (use sparingly)
  ```python
  logger.critical("Database connection lost")
  ```

## Environment Configuration

### Development Settings

For local development, create a `.env` file:

```bash
DEBUG=True
SECRET_KEY=your-dev-secret-key
# ... other settings
```

This will:
- Enable DEBUG-level logging to console
- Show detailed error pages
- Log all SQL queries to `iims_db.log`

### Production Settings

For production, set:

```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com
# ... other settings
```

This will:
- Enable INFO-level logging only
- Suppress DEBUG logs for better performance
- Reduce database query logging

### Additional Logging Settings

You can customize logging behavior with environment variables:

```bash
# Database readiness check settings
DB_READINESS_MAX_RETRIES=5
DB_READINESS_BACKOFF_BASE=0.5
```

## Monitoring and Debugging

### View Recent Logs

```bash
# View all recent logs
tail -f logs/iims.log

# View only errors
tail -f logs/iims_errors.log

# View database logs
tail -f logs/iims_db.log

# Search for specific request
grep "request-id-here" logs/iims.log
```

### Common Debugging Scenarios

#### Scenario 1: User Login Issues

1. Check request logs for login attempts
2. Look for WARNING or ERROR messages in that timeframe
3. Trace the request ID through authentication flow

```bash
grep "login" logs/iims.log | tail -20
```

#### Scenario 2: Translation Failures

1. Search for translation-related logs
2. Check for AI service availability errors
3. Verify Groq API key configuration

```bash
grep "translation" logs/iims.log -i
grep "GROQ" logs/iims_errors.log
```

#### Scenario 3: RSS Ingestion Problems

1. Check ingestion logs for specific sources
2. Look for feed parsing errors
3. Verify source URLs and accessibility

```bash
grep "ingestion" logs/iims.log
grep "RSS source" logs/iims.log
```

### Log Analysis Tips

1. **Use timestamps** to correlate events
2. **Search by request ID** to trace user actions
3. **Filter by level** to focus on errors: `grep "\[ERROR\]" logs/iims.log`
4. **Monitor patterns** to identify recurring issues
5. **Check both console and file logs** as they may have different verbosity

## Best Practices

### When Adding New Logging

1. **Choose the appropriate level**: Don't log everything as ERROR
2. **Include context**: User, action, resource IDs
3. **Use request context**: Call `_log_with_request()` in views
4. **Be concise**: Log messages should be clear but not verbose
5. **Avoid sensitive data**: Don't log passwords, tokens, or PII

### Examples

✅ **Good logging**:
```python
_log_with_request(
    request, logging.INFO,
    f"User {request.user.username} created report {report.id}"
)
```

❌ **Bad logging**:
```python
# Too verbose, no context, wrong level
logger.error(f"Did something with some data {entire_object.__dict__}")
```

✅ **Good error logging**:
```python
except Exception as e:
    _log_with_request(
        request, logging.ERROR,
        f"Failed to process report {report_id}: {str(e)}"
    )
```

❌ **Bad error logging**:
```python
except Exception as e:
    pass  # Silent failure!
```

## Troubleshooting

### Logs not appearing?

1. Check that the `logs/` directory exists and is writable
2. Verify `DEBUG` setting in `.env`
3. Ensure the logger name matches your module (`core`, `intelligence`, etc.)

### Log files growing too large?

The system uses rotating file handlers that automatically:
- Rotate files when they reach max size (10MB for most files)
- Keep only the configured number of backups
- You can adjust these in `config/settings.py` if needed

### Request ID not appearing?

1. Ensure `RequestIDMiddleware` is in `MIDDLEWARE` setting
2. Verify `RequestIDFilter` is in logger configuration
3. Check that you're using `_log_with_request()` helper in views

## Security Considerations

- ⚠️ **Never log sensitive data**: passwords, API keys, tokens, credit card numbers
- ⚠️ **Be careful with PII**: avoid logging personal information in detail
- ⚠️ **Protect log files**: ensure proper file permissions on production servers
- ⚠️ **Monitor log access**: track who accesses log files in production

## Additional Resources

- Django Logging Documentation: https://docs.djangoproject.com/en/6.0/topics/logging/
- Python Logging Cookbook: https://docs.python.org/3/howto/logging-cookbook.html
- IIMS Project README: [README.md](README.md)

## Support

For questions or issues related to logging:
1. Check this guide first
2. Review recent logs for error messages
3. Consult the development team
4. Open an issue in the project repository
