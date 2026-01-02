# IIMS-System

نظام إدارة المعلومات الاستخباراتية (Intelligence Information Management System)

## Overview

Django-based intelligence platform for managing, ingesting, and analyzing reports and sources with built-in audit logging and Arabic language support.

## Features

- **Custom User Authentication**: QR code login, staff roles, custom user model
- **Intelligence Reports**: Ingest and manage intelligence reports with rich metadata
- **Source Management**: Track and manage intelligence sources
- **Audit Logging**: Complete action audit trail for compliance
- **Arabic UI**: RTL-friendly templates and localization (ar-SA)
- **Static File Serving**: WhiteNoise integration for production deployment

## Tech Stack

- **Framework**: Django 5.0.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Static Files**: WhiteNoise
- **AI Engine**: Groq (for translation and analysis)
- **Language**: Arabic (ar-SA), localized to Asia/Riyadh timezone
- **Deployment**: Railway, Render, Vercel, Docker

## Project Structure

```
├── config/              # Django project settings
├── core/                # User auth, custom User model, audit logging
├── intelligence/        # Reports, sources, analysis, ingestion
├── manage.py            # Django management CLI
├── requirements.txt     # Project dependencies
├── db.sqlite3           # SQLite database (development)
└── media/               # Uploaded files (QR codes, user avatars)
```

## Quick Start

### Prerequisites
- Python 3.9+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/FASIL702/IIMS-System.git
cd IIMS-System
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create superuser (staff):
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

Navigate to `http://localhost:8000/` to access the application.

## Management Commands

### Initialize Security User
```bash
python manage.py init_sec_user
```
Creates a default security user for QR login testing.

### Setup Roles
```bash
python manage.py setup_roles
```
Initializes user roles and permissions.

### Ingest News
```bash
python manage.py ingest_news
```
Ingests news data into intelligence reports.

## Authentication

### Standard Login
Visit `/login/` and enter credentials.

### QR Code Login
POST JSON to `/login/qr/` with format:
```json
{
  "qr_data": "USER:username|JOB:job_number|UID:user_id"
}
```

## Audit Logging

All user actions are logged via `UserActionLog` model:
- Login / Logout
- Report views
- User management actions
- Admin operations

Access audit logs at `/audit/` (staff only).

## Configuration

Key settings in `config/settings.py`:
- `AUTH_USER_MODEL = 'core.User'`
- `LANGUAGE_CODE = 'ar'`
- `TIME_ZONE = 'Asia/Riyadh'`
- `ALLOWED_HOSTS = ['*']` (production: restrict)
- `CSRF_TRUSTED_ORIGINS` for Azure deployment

## Testing

Run Django test suite:
```bash
python manage.py test
```

Test files:
- `core/tests*.py` — user, auth, audit logging tests
- `intelligence/tests*.py` — report, source, analysis tests

## 🚀 Deployment

IIMS System is production-ready and can be deployed on multiple platforms.

### Quick Deploy Options

#### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

**Why Railway?**
- ✅ Easy setup with PostgreSQL included
- ✅ Automatic deployments from GitHub
- ✅ Free SSL certificates
- ✅ Built-in monitoring and logs
- ✅ Affordable pricing ($5/month)

**Quick Start:**
1. Click the button above
2. Connect your GitHub repository
3. Add environment variables (see below)
4. Deploy!

📖 **Detailed Guide**: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

---

#### Render
**Steps:**
1. Create account at [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repository
4. Configure:
   - Build Command: `bash build.sh`
   - Start Command: `bash startup.sh`
5. Add PostgreSQL database
6. Set environment variables
7. Deploy

---

#### Docker
```bash
# Build image
docker build -t iims-system:latest .

# Run container
docker run -d \
  --name iims-system \
  -p 8004:8004 \
  -e SECRET_KEY="your-secret-key" \
  -e DATABASE_URL="postgresql://..." \
  -e ADMIN_PASSWORD="your-password" \
  iims-system:latest
```

---

### Environment Variables

#### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `DEBUG` | Debug mode (False in production) | `False` |
| `ALLOWED_HOSTS` | Allowed domains | `myapp.railway.app` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `ADMIN_PASSWORD` | Admin user password | `SecurePassword123!` |

#### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq AI API key for translation | None |
| `GROQ_MODEL` | AI model to use | `llama-3.3-70b-versatile` |
| `WEB_CONCURRENCY` | Number of Gunicorn workers | `3` |
| `PORT` | Application port | `8004` |

📖 **Complete Documentation**: 
- [DEPLOYMENT.md](DEPLOYMENT.md) - Comprehensive deployment guide
- [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md) - All environment variables
- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Railway-specific guide

---

### Health Checks

The system includes built-in health check endpoints:

```bash
# Basic health check
GET /health/

# Detailed health check (staff only)
GET /health/detailed/

# Kubernetes-style probes
GET /health/ready/
GET /health/live/
```

**Python Health Check Script:**
```bash
python health_check.py
```

This will verify:
- ✅ Database connectivity
- ✅ Migrations status
- ✅ Static files
- ✅ Environment variables
- ✅ Security settings
- ✅ Groq AI integration

## API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home / redirect to dashboard |
| `/login/` | GET, POST | User login page |
| `/login/qr/` | POST | QR code login endpoint |
| `/logout/` | GET | User logout |

### Intelligence
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/intelligence/dashboard/` | GET | Intelligence dashboard (auth required) |
| `/intelligence/report/<id>/` | GET | View intelligence report |
| `/intelligence/sources/` | GET | Source management |
| `/intelligence/analysis/` | GET | Analysis tools |

### Admin & Monitoring
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/` | GET | Admin panel (staff only) |
| `/audit/` | GET | Audit log (staff only) |
| `/health/` | GET | Health check endpoint |
| `/health/detailed/` | GET | Detailed health check (staff only) |
| `/health/ready/` | GET | Readiness probe |
| `/health/live/` | GET | Liveness probe |

### AI Agent
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/` | GET | AI agent interface |
| `/agent/chat/` | POST | Chat with AI agent |
| `/health/llm/` | GET | LLM health check |

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add your feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

## License

This project is proprietary. All rights reserved.

## Contact

For questions or issues, contact the project maintainer or create an issue on GitHub.
