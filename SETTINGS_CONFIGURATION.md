# Django Settings Configuration Guide

## Overview

The Django settings have been updated to properly support both development and production environments using environment variables. This addresses the configuration issues related to SECRET_KEY, ALLOWED_HOSTS, and database connectivity.

## Key Features

### 1. SECRET_KEY Management
- **Development**: Falls back to insecure development key when `DEBUG=True` and `SECRET_KEY` is not set
- **Production**: **REQUIRED** from environment variable when `DEBUG=False`
- Raises `ValueError` if `SECRET_KEY` is missing in production mode

```bash
# Generate a new SECRET_KEY:
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 2. ALLOWED_HOSTS Configuration
- **Development**: Automatically set to `['127.0.0.1', 'localhost', '0.0.0.0']`
- **Production**: Can be configured via:
  - `ALLOWED_HOSTS` environment variable (comma-separated)
  - Auto-detected from platform variables:
    - Railway: `RAILWAY_PUBLIC_DOMAIN`
    - Render: `RENDER_EXTERNAL_HOSTNAME`
    - Vercel: `VERCEL_URL`
- Raises `ValueError` if empty in production mode

### 3. Database Configuration
- **Development**: SQLite (default, no configuration needed)
- **Production**: PostgreSQL via `DATABASE_URL` environment variable

#### Database Timeout Settings
The following environment variables control database connection behavior:

- `DB_CONN_MAX_AGE`: Connection pool timeout in seconds (default: 600)
- `DB_CONNECT_TIMEOUT`: Connection establishment timeout in seconds (default: 10)
- `DB_SSL_REQUIRE`: Require SSL for database connections (default: False)

```bash
# Example DATABASE_URL
DATABASE_URL=postgresql://user:password@host:5432/database
DB_CONN_MAX_AGE=600
DB_CONNECT_TIMEOUT=10
```

### 4. Security Settings (Production Only)
When `DEBUG=False`, the following security settings are automatically enabled:

- `SECURE_SSL_REDIRECT`: True (redirect HTTP to HTTPS)
- `SECURE_HSTS_SECONDS`: 31536000 (1 year)
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`: True
- `SECURE_HSTS_PRELOAD`: True
- `SESSION_COOKIE_SECURE`: True
- `CSRF_COOKIE_SECURE`: True
- `SECURE_BROWSER_XSS_FILTER`: True
- `SECURE_CONTENT_TYPE_NOSNIFF`: True
- `X_FRAME_OPTIONS`: 'DENY'

All can be overridden via environment variables.

### 5. CSRF Trusted Origins
- **Development**: Empty (not needed)
- **Production**: Auto-detected from platform variables or manual configuration

```bash
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
```

### 6. Language and Timezone
- `LANGUAGE_CODE`: Default 'ar' (Arabic), configurable via environment
- `TIME_ZONE`: Default 'Asia/Riyadh', configurable via environment

## Environment Variable Reference

### Required for Production

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes (prod) | Development fallback | Django secret key for cryptographic signing |
| `DEBUG` | No | True | Enable/disable debug mode |
| `ALLOWED_HOSTS` | Yes (prod) | Auto-detect | Comma-separated list of allowed hostnames |

### Database Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | No | SQLite | PostgreSQL connection URL |
| `DB_CONN_MAX_AGE` | No | 600 | Connection pool timeout (seconds) |
| `DB_CONNECT_TIMEOUT` | No | 10 | Connection timeout (seconds) |
| `DB_SSL_REQUIRE` | No | False | Require SSL for database connections |

### Platform Auto-Detection

| Variable | Source | Description |
|----------|--------|-------------|
| `RAILWAY_PUBLIC_DOMAIN` | Railway | Auto-added to ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS |
| `RENDER_EXTERNAL_HOSTNAME` | Render | Auto-added to ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS |
| `RENDER_EXTERNAL_URL` | Render | Auto-added to CSRF_TRUSTED_ORIGINS |
| `VERCEL_URL` | Vercel | Auto-added to ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `LANGUAGE_CODE` | ar | Application language |
| `TIME_ZONE` | Asia/Riyadh | Application timezone |
| `CSRF_TRUSTED_ORIGINS` | Auto-detect | Comma-separated HTTPS origins |

## Example Configurations

### Local Development

```bash
# .env file (optional, uses defaults)
DEBUG=True
# SECRET_KEY not needed - uses fallback
# Database not needed - uses SQLite
```

### Production (Railway)

```bash
# .env file
SECRET_KEY=your-generated-secret-key-at-least-50-chars-long
DEBUG=False
ALLOWED_HOSTS=myapp.railway.app
DATABASE_URL=postgresql://user:pass@host:5432/railway
# RAILWAY_PUBLIC_DOMAIN is auto-provided by Railway
```

### Production (Manual)

```bash
# .env file
SECRET_KEY=your-generated-secret-key-at-least-50-chars-long
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com,api.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
DATABASE_URL=postgresql://user:pass@host:5432/database
DB_CONN_MAX_AGE=1200
DB_CONNECT_TIMEOUT=30
```

## Validation

### Check Development Configuration

```bash
python manage.py check
```

### Check Production Configuration

```bash
DEBUG=False SECRET_KEY=test-key ALLOWED_HOSTS=example.com python manage.py check --deploy
```

### Run Configuration Tests

```bash
python manage.py test config.tests
```

## Troubleshooting

### Error: "SECRET_KEY environment variable is required in production"

**Solution**: Set `SECRET_KEY` environment variable or set `DEBUG=True` for development.

```bash
export SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
```

### Error: "ALLOWED_HOSTS must be configured in production"

**Solution**: Set `ALLOWED_HOSTS` environment variable or ensure platform variables are available.

```bash
export ALLOWED_HOSTS=example.com,www.example.com
```

### Database Connection Timeout

**Solution**: Adjust database timeout settings:

```bash
export DB_CONNECT_TIMEOUT=30  # Increase connection timeout
export DB_CONN_MAX_AGE=1200   # Increase connection pool timeout
```

## Migration from Old Settings

If you were using the old settings.py without environment variable support:

1. **Generate a SECRET_KEY**:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Set environment variables** in your deployment platform:
   - `SECRET_KEY`: The generated key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: Your domain(s)

3. **Test the configuration**:
   ```bash
   python manage.py check --deploy
   ```

4. **Deploy**: The application will now properly validate all required settings.

## References

- Django Settings Documentation: https://docs.djangoproject.com/en/5.0/ref/settings/
- Django Deployment Checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- Environment Variables Documentation: See `.env.production.example` in repository
