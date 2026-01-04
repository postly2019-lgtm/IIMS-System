"""
Tests for Django settings configuration.

These tests verify that the settings.py properly handles environment variables
and configuration for both development and production environments.
"""

import os
import subprocess
import sys
import json
from pathlib import Path
from unittest import TestCase


class SettingsConfigurationTests(TestCase):
    """Test settings configuration with various environment variables."""
    
    def _test_settings_with_env(self, env_vars, expected_checks):
        """
        Helper to test settings with specific environment variables.
        Runs a subprocess to avoid polluting current environment.
        """
        # Use JSON to safely pass environment variables to avoid injection
        test_script = """
import os
import sys
import json

# Load environment variables from JSON
env_data = json.loads({env_json})
for key, value in env_data.items():
    os.environ[key] = value

try:
    from config import settings
    print("SUCCESS")
    {checks}
except Exception as e:
    print("ERROR:", str(e))
    sys.exit(1)
"""
        env_json = json.dumps(json.dumps(env_vars))  # Double encode for safe embedding
        checks = '\n    '.join([f"print({json.dumps(key + ':')}, {value})" for key, value in expected_checks.items()])
        
        full_script = test_script.format(env_json=env_json, checks=checks)
        
        result = subprocess.run(
            [sys.executable, '-c', full_script],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )
        
        return result.returncode, result.stdout, result.stderr
    
    def test_secret_key_from_environment(self):
        """Test that SECRET_KEY is loaded from environment variable."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-secret-key', 'DEBUG': 'True'},
            {'SECRET_KEY': 'settings.SECRET_KEY'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('SUCCESS', stdout)
        self.assertIn('test-secret-key', stdout)
    
    def test_secret_key_fallback_in_debug(self):
        """Test that SECRET_KEY falls back to default when DEBUG=True."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DEBUG': 'True'},
            {'SECRET_KEY_SET': 'bool(settings.SECRET_KEY)', 
             'SECRET_KEY_LENGTH': 'len(settings.SECRET_KEY)'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('SUCCESS', stdout)
        self.assertIn('SECRET_KEY_SET: True', stdout)
        # Verify the key is reasonably long (not empty or too short)
        # This tests behavior without coupling to specific implementation
        output_lines = stdout.split('\n')
        for line in output_lines:
            if 'SECRET_KEY_LENGTH:' in line:
                length = int(line.split(':')[1].strip())
                self.assertGreater(length, 20, "Fallback SECRET_KEY should be reasonably long")
    
    def test_secret_key_required_in_production(self):
        """Test that SECRET_KEY is required when DEBUG=False."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DEBUG': 'False'},
            {}
        )
        self.assertNotEqual(returncode, 0, "Should fail without SECRET_KEY")
        self.assertIn('SECRET_KEY environment variable is required', stdout + stderr)
    
    def test_debug_true_by_default(self):
        """Test that DEBUG defaults to True if not set."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {},
            {'DEBUG': 'settings.DEBUG'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('DEBUG: True', stdout)
    
    def test_debug_false_from_environment(self):
        """Test that DEBUG can be set to False via environment."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-key', 'DEBUG': 'False', 'ALLOWED_HOSTS': 'example.com'},
            {'DEBUG': 'settings.DEBUG'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('DEBUG: False', stdout)
    
    def test_allowed_hosts_in_development(self):
        """Test that ALLOWED_HOSTS includes localhost in development."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DEBUG': 'True'},
            {'ALLOWED_HOSTS': 'settings.ALLOWED_HOSTS'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('127.0.0.1', stdout)
        self.assertIn('localhost', stdout)
    
    def test_allowed_hosts_from_environment(self):
        """Test that ALLOWED_HOSTS is parsed from environment variable."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-key', 'DEBUG': 'False', 
             'ALLOWED_HOSTS': 'example.com,www.example.com'},
            {'ALLOWED_HOSTS': 'settings.ALLOWED_HOSTS'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('example.com', stdout)
        self.assertIn('www.example.com', stdout)
    
    def test_allowed_hosts_railway_auto_detect(self):
        """Test that ALLOWED_HOSTS auto-detects Railway domain."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-key', 'DEBUG': 'False', 
             'RAILWAY_PUBLIC_DOMAIN': 'myapp.railway.app'},
            {'ALLOWED_HOSTS': 'settings.ALLOWED_HOSTS'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('myapp.railway.app', stdout)
    
    def test_allowed_hosts_required_in_production(self):
        """Test that ALLOWED_HOSTS is required when DEBUG=False."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-key', 'DEBUG': 'False'},
            {}
        )
        self.assertNotEqual(returncode, 0, "Should fail without ALLOWED_HOSTS")
        self.assertIn('ALLOWED_HOSTS must be configured', stdout + stderr)
    
    def test_database_url_postgres(self):
        """Test that DATABASE_URL is parsed for PostgreSQL."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DATABASE_URL': 'postgresql://user:pass@localhost:5432/testdb'},
            {'DB_ENGINE': 'settings.DATABASES["default"]["ENGINE"]',
             'DB_NAME': 'settings.DATABASES["default"]["NAME"]'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('postgresql', stdout)
        self.assertIn('testdb', stdout)
    
    def test_database_fallback_to_sqlite(self):
        """Test that database falls back to SQLite when no DATABASE_URL."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {},
            {'DB_ENGINE': 'settings.DATABASES["default"]["ENGINE"]'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('sqlite3', stdout)
    
    def test_database_conn_max_age_default(self):
        """Test that database connection max age has a default value."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DATABASE_URL': 'postgresql://user:pass@localhost:5432/testdb'},
            {'CONN_MAX_AGE': 'settings.DATABASES["default"]["CONN_MAX_AGE"]'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('CONN_MAX_AGE: 600', stdout)
    
    def test_database_conn_max_age_custom(self):
        """Test that database connection max age can be customized."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DATABASE_URL': 'postgresql://user:pass@localhost:5432/testdb',
             'DB_CONN_MAX_AGE': '300'},
            {'CONN_MAX_AGE': 'settings.DATABASES["default"]["CONN_MAX_AGE"]'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('CONN_MAX_AGE: 300', stdout)
    
    def test_database_connect_timeout(self):
        """Test that database connection timeout is set for PostgreSQL."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DATABASE_URL': 'postgresql://user:pass@localhost:5432/testdb'},
            {'CONNECT_TIMEOUT': 'settings.DATABASES["default"]["OPTIONS"]["connect_timeout"]'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('CONNECT_TIMEOUT: 10', stdout)
    
    def test_database_connect_timeout_custom(self):
        """Test that database connection timeout can be customized."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'DATABASE_URL': 'postgresql://user:pass@localhost:5432/testdb',
             'DB_CONNECT_TIMEOUT': '20'},
            {'CONNECT_TIMEOUT': 'settings.DATABASES["default"]["OPTIONS"]["connect_timeout"]'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('CONNECT_TIMEOUT: 20', stdout)
    
    def test_csrf_trusted_origins_in_production(self):
        """Test that CSRF_TRUSTED_ORIGINS is configured in production."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-key', 'DEBUG': 'False', 'ALLOWED_HOSTS': 'example.com',
             'CSRF_TRUSTED_ORIGINS': 'https://example.com,https://www.example.com'},
            {'CSRF_ORIGINS': 'settings.CSRF_TRUSTED_ORIGINS'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('https://example.com', stdout)
    
    def test_csrf_trusted_origins_railway_auto_detect(self):
        """Test that CSRF_TRUSTED_ORIGINS auto-detects Railway domain."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-key', 'DEBUG': 'False', 
             'RAILWAY_PUBLIC_DOMAIN': 'myapp.railway.app'},
            {'CSRF_ORIGINS': 'settings.CSRF_TRUSTED_ORIGINS'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('https://myapp.railway.app', stdout)
    
    def test_security_settings_in_production(self):
        """Test that security settings are enabled in production."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {'SECRET_KEY': 'test-key', 'DEBUG': 'False', 'ALLOWED_HOSTS': 'example.com'},
            {
                'SSL_REDIRECT': 'settings.SECURE_SSL_REDIRECT',
                'HSTS_SECONDS': 'settings.SECURE_HSTS_SECONDS',
                'SESSION_SECURE': 'settings.SESSION_COOKIE_SECURE',
                'CSRF_SECURE': 'settings.CSRF_COOKIE_SECURE',
            }
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('SSL_REDIRECT: True', stdout)
        self.assertIn('HSTS_SECONDS: 31536000', stdout)
        self.assertIn('SESSION_SECURE: True', stdout)
        self.assertIn('CSRF_SECURE: True', stdout)
    
    def test_auth_user_model_configured(self):
        """Test that AUTH_USER_MODEL is set to custom User model."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {},
            {'AUTH_USER_MODEL': 'settings.AUTH_USER_MODEL'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('AUTH_USER_MODEL: core.User', stdout)
    
    def test_language_and_timezone_defaults(self):
        """Test that LANGUAGE_CODE and TIME_ZONE have proper defaults."""
        returncode, stdout, stderr = self._test_settings_with_env(
            {},
            {'LANGUAGE': 'settings.LANGUAGE_CODE', 'TIMEZONE': 'settings.TIME_ZONE'}
        )
        self.assertEqual(returncode, 0, f"Script failed: {stderr}")
        self.assertIn('LANGUAGE: ar', stdout)
        self.assertIn('TIMEZONE: Asia/Riyadh', stdout)

