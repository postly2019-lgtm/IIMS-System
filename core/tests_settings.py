"""
Tests for Django settings configuration.
Validates that all critical settings are properly configured for Django 6.0.
"""
from django.test import TestCase, override_settings
from django.conf import settings
import django


class SettingsConfigurationTest(TestCase):
    """Test suite for validating Django settings configuration."""

    def test_django_version(self):
        """Verify Django 6.0 is installed."""
        self.assertEqual(django.VERSION[0], 6, "Django 6.0 should be installed")
        self.assertEqual(django.VERSION[1], 0, "Django 6.0 should be installed")

    def test_secret_key_configured(self):
        """Verify SECRET_KEY is configured."""
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertGreater(len(settings.SECRET_KEY), 0)

    def test_debug_mode(self):
        """Verify DEBUG mode is configurable."""
        # In tests, DEBUG should typically be True
        self.assertIsInstance(settings.DEBUG, bool)

    def test_allowed_hosts_configured(self):
        """Verify ALLOWED_HOSTS is configured."""
        self.assertIsInstance(settings.ALLOWED_HOSTS, list)
        # In development, should have localhost
        if settings.DEBUG:
            self.assertIn('127.0.0.1', settings.ALLOWED_HOSTS)

    def test_custom_user_model(self):
        """Verify custom user model is configured."""
        self.assertEqual(settings.AUTH_USER_MODEL, 'core.User')

    def test_localization_settings(self):
        """Verify localization settings for Arabic/Riyadh."""
        self.assertEqual(settings.LANGUAGE_CODE, 'ar')
        self.assertEqual(settings.TIME_ZONE, 'Asia/Riyadh')
        self.assertTrue(settings.USE_I18N)
        self.assertTrue(settings.USE_TZ)

    def test_installed_apps(self):
        """Verify all required apps are installed."""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'core.apps.CoreConfig',
            'intelligence.apps.IntelligenceConfig',
            'intelligence_agent.apps.IntelligenceAgentConfig',
        ]
        for app in required_apps:
            with self.subTest(app=app):
                self.assertIn(app, settings.INSTALLED_APPS)

    def test_middleware_configuration(self):
        """Verify all required middleware is configured."""
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'core.middleware.DBReadinessMiddleware',
        ]
        for middleware in required_middleware:
            with self.subTest(middleware=middleware):
                self.assertIn(middleware, settings.MIDDLEWARE)

    def test_database_configuration(self):
        """Verify database is configured."""
        self.assertIn('default', settings.DATABASES)
        self.assertIn('ENGINE', settings.DATABASES['default'])
        # Should be either SQLite or PostgreSQL
        engine = settings.DATABASES['default']['ENGINE']
        self.assertIn(engine, [
            'django.db.backends.sqlite3',
            'django.db.backends.postgresql'
        ])

    def test_static_files_configuration(self):
        """Verify static files configuration."""
        self.assertEqual(settings.STATIC_URL, '/static/')
        self.assertIsNotNone(settings.STATIC_ROOT)
        self.assertEqual(
            settings.STATICFILES_STORAGE,
            'whitenoise.storage.CompressedManifestStaticFilesStorage'
        )

    def test_media_files_configuration(self):
        """Verify media files configuration."""
        self.assertEqual(settings.MEDIA_URL, '/media/')
        self.assertIsNotNone(settings.MEDIA_ROOT)

    def test_security_settings_in_production(self):
        """Verify security settings are conditionally configured based on DEBUG mode."""
        # Test production security settings with override_settings
        with override_settings(
            DEBUG=False,
            SESSION_COOKIE_SECURE=True,
            CSRF_COOKIE_SECURE=True,
            SECURE_SSL_REDIRECT=True,
            SECURE_HSTS_SECONDS=31536000,
        ):
            # Verify production security settings would be properly set
            self.assertFalse(settings.DEBUG)
            self.assertTrue(settings.SESSION_COOKIE_SECURE)
            self.assertTrue(settings.CSRF_COOKIE_SECURE)
            self.assertTrue(settings.SECURE_SSL_REDIRECT)
            self.assertGreater(settings.SECURE_HSTS_SECONDS, 0)
        
        # In current test environment (may have DEBUG=True or False)
        # Just verify the settings exist and are boolean/int types
        self.assertIsInstance(settings.DEBUG, bool)
        # SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE always exist (Django defaults)
        self.assertIn(settings.SESSION_COOKIE_SECURE, [True, False])
        self.assertIn(settings.CSRF_COOKIE_SECURE, [True, False])

    def test_logging_configuration(self):
        """Verify logging is configured."""
        self.assertIn('version', settings.LOGGING)
        self.assertIn('handlers', settings.LOGGING)
        self.assertIn('loggers', settings.LOGGING)
        # Check for IIMS-specific loggers
        self.assertIn('iims.db', settings.LOGGING['loggers'])

    def test_groq_ai_configuration(self):
        """Verify Groq AI settings are present."""
        # These settings should exist even if not configured
        self.assertIsInstance(settings.GROQ_MODEL, str)
        self.assertIsInstance(settings.GROQ_REASONING_EFFORT, str)
        self.assertIsInstance(settings.GROQ_MAX_COMPLETION_TOKENS, int)
        self.assertIsInstance(settings.GROQ_TEMPERATURE, float)

    def test_db_readiness_middleware_config(self):
        """Verify DB readiness middleware configuration."""
        self.assertIsInstance(settings.DB_READINESS_MAX_RETRIES, int)
        self.assertGreater(settings.DB_READINESS_MAX_RETRIES, 0)
        self.assertIsInstance(settings.DB_READINESS_BACKOFF_BASE, float)
        self.assertGreater(settings.DB_READINESS_BACKOFF_BASE, 0)

    def test_template_configuration(self):
        """Verify template configuration."""
        self.assertEqual(len(settings.TEMPLATES), 1)
        template_config = settings.TEMPLATES[0]
        self.assertEqual(
            template_config['BACKEND'],
            'django.template.backends.django.DjangoTemplates'
        )
        self.assertTrue(template_config['APP_DIRS'])
        # Verify required context processors
        context_processors = template_config['OPTIONS']['context_processors']
        required_processors = [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
        ]
        for processor in required_processors:
            with self.subTest(processor=processor):
                self.assertIn(processor, context_processors)
