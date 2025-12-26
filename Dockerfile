# 1. Base Image
FROM python:3.11-slim-bookworm

# 2. Environment Setup (The "Single Source of Truth" Context)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Create a virtual environment to isolate dependencies explicitly
    VIRTUAL_ENV=/opt/venv

# Add virtual environment to PATH
# This ensures that 'python' and 'pip' commands ALWAYS use the venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 3. Work Directory
WORKDIR /app

# 4. System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Build Dependencies (Dependency Layer)
# We create the venv and install dependencies FIRST
RUN python -m venv $VIRTUAL_ENV
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 6. Application Code (Source Layer)
COPY . .

# 7. Verification & Build Integrity Check
# Explicitly verify Django is importable in THIS environment before proceeding
RUN python -c "import django; print(f'Django {django.get_version()} is successfully installed in {django.__path__}')"

# 8. Static Files (Framework Management Command)
# We run this ONLY after dependencies and code are fully present
# We provide dummy environment variables to satisfy settings.py import
RUN SECRET_KEY=build-time-insecure-key \
    DEBUG=False \
    DATABASE_URL=sqlite:///db.sqlite3 \
    python manage.py collectstatic --noinput

# 9. Runtime Execution
# Use the same 'python' (which is the venv python due to PATH)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
