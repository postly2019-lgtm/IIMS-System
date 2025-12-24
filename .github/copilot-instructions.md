# Copilot instructions for IIMS-System

Purpose: give AI coding agents the minimal, actionable knowledge to be productive in this Django codebase.

- **Project type:** Django (generated with Django 6.0). Entrypoint: `manage.py`.
- **Apps:** `core` (custom user model, auth, admin, audit logging) and `intelligence` (ingestion, reports, analysis).
- **Settings:** see `config/settings.py` for critical runtime choices: `AUTH_USER_MODEL='core.User'`, `LANGUAGE_CODE='ar'`, `TIME_ZONE='Asia/Riyadh'`, `STATICFILES_STORAGE` uses `whitenoise`.
- **DB & deps:** default DB is SQLite (`db.sqlite3`). `requirements.txt` only lists `whitenoise`; the repo relies on a Python virtualenv in `venv/` during development; assume Django and common libs are installed in the environment.

Key files and conventions (examples):

- Authentication & QR login: `core/views.py` implements `qr_login_view` which parses QR payloads and calls `login(..., backend='django.contrib.auth.backends.ModelBackend')`. Review `core/models.py` and `core/forms.py` for the custom `User` and `UserForm` contract.
- Audit logging: controllers call `UserActionLog.objects.create(...)` (see `core/views.py`, `intelligence/views.py`). Use that pattern when adding new user-visible actions.
- Templates: per-app templates live under `core/templates/core/` and `intelligence/templates/intelligence/` — follow existing Arabic strings, RTL layouts and filenames (`card.html`, `dashboard.html`, `report_detail.html`).
- Management commands: bootstrap and ingestion commands live under `core/management/commands/` and `intelligence/management/commands/` (e.g. `init_sec_user.py`, `ingest_news.py`). Use `python manage.py <command>` to run them.

Developer workflows (how-to):

- Run locally (assumes Python venv):

  - Create & activate venv, install dependencies (Django 6.x required but not pinned in `requirements.txt`):

    pip install django==6.0 whitenoise

  - Apply migrations and run server:

    python manage.py migrate
    python manage.py runserver

- Tests: run Django tests with `python manage.py test`. Relevant test files: `core/tests*.py`, `intelligence/tests*.py`.
- Static & media: static files served via `whitenoise` in production; media files are stored under the `media/` folder (see `MEDIA_ROOT` in `config/settings.py`).
- Deployment hints: `vercel.json` and `startup.sh` exist; the app uses `whitenoise` and allows all hosts (`ALLOWED_HOSTS=['*']`) and includes `CSRF_TRUSTED_ORIGINS` for Azure — check these when preparing production deploys.

Project-specific patterns to follow (concrete):

- Use `UserActionLog` for any action that should be auditable — controllers and views explicitly create logs with `action`, `target_object`, `details`, `ip_address`.
- Views that require staff use the `@user_passes_test(lambda u: u.is_staff)` decorator (see `core/views.py`). Follow this when adding admin-only pages.
- Naming & routes: URLs often use named routes like `login`, `dashboard`, `user_list`. The QR login returns `/intel/dashboard/` on success — map to existing intelligence dashboard route.
- Keep RTL/Arabic UI in mind: strings, templates, and templates' titles are in Arabic (see `core/user_form.html` titles in views).

Integration points & gotchas discovered:

- `AUTH_USER_MODEL` is `core.User` — any migration or data access must reference that model via `get_user_model()`.
- The `qr_login_view` intentionally logs in users directly using a QR payload; review security implications before changing.
- `requirements.txt` is sparse; rely on the repository's `venv/` for installed packages or add a fuller `requirements.txt` when updating dependencies.

When editing code, useful files to inspect first:

- [config/settings.py](config/settings.py)
- [manage.py](manage.py)
- [core/views.py](core/views.py)
- [core/models.py](core/models.py)
- [core/management/commands/init_sec_user.py](core/management/commands/init_sec_user.py)
- [intelligence/views.py](intelligence/views.py)
- [intelligence/management/commands/ingest_news.py](intelligence/management/commands/ingest_news.py)

If anything here is unclear or you want deeper detail (routing map, model fields, or test coverage), tell me which area to expand and I'll update this file.
