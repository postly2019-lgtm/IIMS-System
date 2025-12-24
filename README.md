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

- **Framework**: Django 6.0
- **Database**: SQLite (development) / configurable for production
- **Static Files**: WhiteNoise
- **Language**: Arabic (ar-SA), localized to Asia/Riyadh timezone
- **Deployment**: Vercel-ready (see `vercel.json`, `startup.sh`)

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
pip install django==6.0 whitenoise
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

## Deployment

### Vercel
- `vercel.json` configured for Django app
- `startup.sh` runs migrations and static collection
- Uses `whitenoise` for static file serving
- Azure integration via `CSRF_TRUSTED_ORIGINS`

### Local WSGI
```bash
python -m gunicorn config.wsgi:application
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DEBUG` | 'True' | Django debug mode (set to False in production) |
| `SECRET_KEY` | (insecure default) | Django secret key (override in production) |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home / redirect to dashboard |
| `/login/` | GET, POST | User login page |
| `/login/qr/` | POST | QR code login endpoint |
| `/logout/` | GET | User logout |
| `/intel/dashboard/` | GET | Intelligence dashboard (auth required) |
| `/intel/report/<id>/` | GET | View intelligence report |
| `/admin/` | GET | Admin panel (staff only) |
| `/audit/` | GET | Audit log (staff only) |

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add your feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

## License

This project is proprietary. All rights reserved.

## Contact

For questions or issues, contact the project maintainer or create an issue on GitHub.
