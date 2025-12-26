# 1. Base Image: Unified Python Environment
FROM python:3.10-slim

# 2. Environment Variables
# Set PYTHONPATH to ensuring the same environment executes manage.py
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
# Default build-time key (will be overridden in production)
ENV SECRET_KEY=build-time-insecure-key
ENV DEBUG=False

# 3. Work Directory (Project Path Integrity)
WORKDIR /app

# 4. System Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Python Dependencies (CRITICAL: Install BEFORE project code/commands)
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy Project Code
COPY . /app/

# 7. Verification & Build-Time Execution
# Verify Django installation and path integrity
RUN python -c "import django; print('Django installed:', django.get_version())"
# Run collectstatic during build (proves manage.py works and dependencies are set)
RUN python manage.py collectstatic --noinput

# 8. Runtime Command
# Only run runtime-specific commands (migrations, server start)
CMD sh -c "python manage.py migrate && python manage.py createsuperuser_if_none_exists && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"
