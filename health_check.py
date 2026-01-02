#!/usr/bin/env python
"""
Health Check Script for IIMS System
سكريبت فحص صحة نظام IIMS

This script performs comprehensive health checks on the IIMS system
to ensure all components are functioning correctly before deployment.

Usage:
    python health_check.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from django.conf import settings
from io import StringIO


class HealthChecker:
    """Comprehensive health checker for IIMS system"""
    
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_check(self, name, status, message=""):
        """Print check result"""
        symbols = {
            'pass': '✅',
            'fail': '❌',
            'warn': '⚠️'
        }
        symbol = symbols.get(status, '❓')
        print(f"{symbol} {name}: {message if message else status.upper()}")
        
        if status == 'pass':
            self.passed.append(name)
        elif status == 'fail':
            self.failed.append(name)
        else:
            self.warnings.append(name)
    
    def check_database(self):
        """Check database connectivity"""
        self.print_header("Database Health Check")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    self.print_check("Database Connection", "pass", "Connected successfully")
                    
                    # Check database type
                    db_engine = settings.DATABASES['default']['ENGINE']
                    if 'postgresql' in db_engine:
                        self.print_check("Database Type", "pass", "PostgreSQL (Production Ready)")
                    elif 'sqlite' in db_engine:
                        self.print_check("Database Type", "warn", "SQLite (Development Only)")
                    else:
                        self.print_check("Database Type", "pass", db_engine)
                else:
                    self.print_check("Database Connection", "fail", "Query returned unexpected result")
        except Exception as e:
            self.print_check("Database Connection", "fail", str(e))
    
    def check_migrations(self):
        """Check if all migrations are applied"""
        self.print_header("Migrations Check")
        try:
            output = StringIO()
            call_command('showmigrations', '--plan', stdout=output)
            migrations_output = output.getvalue()
            
            if '[X]' in migrations_output or '[ ]' not in migrations_output:
                unapplied = migrations_output.count('[ ]')
                if unapplied == 0:
                    self.print_check("Migrations", "pass", "All migrations applied")
                else:
                    self.print_check("Migrations", "warn", f"{unapplied} unapplied migrations found")
            else:
                self.print_check("Migrations", "fail", "No migrations found")
        except Exception as e:
            self.print_check("Migrations", "fail", str(e))
    
    def check_static_files(self):
        """Check static files configuration"""
        self.print_header("Static Files Check")
        try:
            static_root = settings.STATIC_ROOT
            if static_root and os.path.exists(static_root):
                file_count = sum([len(files) for r, d, files in os.walk(static_root)])
                self.print_check("Static Files", "pass", f"{file_count} files in {static_root}")
            else:
                self.print_check("Static Files", "warn", "STATIC_ROOT not found or empty")
            
            # Check WhiteNoise
            if 'whitenoise' in settings.INSTALLED_APPS:
                self.print_check("WhiteNoise", "pass", "Configured")
            else:
                self.print_check("WhiteNoise", "warn", "Not configured")
        except Exception as e:
            self.print_check("Static Files", "fail", str(e))
    
    def check_environment_variables(self):
        """Check critical environment variables"""
        self.print_header("Environment Variables Check")
        
        # Critical variables
        critical_vars = {
            'SECRET_KEY': 'Django secret key',
            'DEBUG': 'Debug mode',
        }
        
        for var, description in critical_vars.items():
            value = os.environ.get(var)
            if value:
                if var == 'SECRET_KEY':
                    # Don't print the actual key
                    display_value = f"Set ({len(value)} chars)"
                    if 'django-insecure' in value.lower():
                        self.print_check(f"{var}", "warn", f"{display_value} - Using insecure default!")
                    else:
                        self.print_check(f"{var}", "pass", display_value)
                elif var == 'DEBUG':
                    if value.lower() == 'false':
                        self.print_check(f"{var}", "pass", "False (Production)")
                    else:
                        self.print_check(f"{var}", "warn", "True (Development)")
                else:
                    self.print_check(f"{var}", "pass", f"Set")
            else:
                self.print_check(f"{var}", "fail", "Not set")
        
        # Optional but recommended
        optional_vars = {
            'ALLOWED_HOSTS': 'Allowed hosts',
            'DATABASE_URL': 'Database URL',
            'GROQ_API_KEY': 'Groq AI API Key',
        }
        
        print("\nOptional Variables:")
        for var, description in optional_vars.items():
            value = os.environ.get(var)
            if value:
                if var == 'GROQ_API_KEY':
                    display_value = f"Set ({len(value)} chars)"
                else:
                    display_value = "Set"
                self.print_check(f"{var}", "pass", display_value)
            else:
                self.print_check(f"{var}", "warn", "Not set")
    
    def check_security_settings(self):
        """Check security settings"""
        self.print_header("Security Settings Check")
        
        security_checks = {
            'SECURE_SSL_REDIRECT': settings.SECURE_SSL_REDIRECT if not settings.DEBUG else None,
            'SECURE_HSTS_SECONDS': getattr(settings, 'SECURE_HSTS_SECONDS', 0),
            'CSRF_COOKIE_SECURE': settings.CSRF_COOKIE_SECURE,
            'SESSION_COOKIE_SECURE': settings.SESSION_COOKIE_SECURE,
        }
        
        for setting, value in security_checks.items():
            if value is None:
                self.print_check(setting, "warn", "Disabled (DEBUG=True)")
            elif value:
                self.print_check(setting, "pass", f"Enabled ({value})")
            else:
                self.print_check(setting, "warn", "Disabled")
    
    def check_installed_apps(self):
        """Check critical installed apps"""
        self.print_header("Installed Apps Check")
        
        critical_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'core',
            'intelligence',
            'intelligence_agent',
        ]
        
        for app in critical_apps:
            if app in settings.INSTALLED_APPS:
                self.print_check(app, "pass", "Installed")
            else:
                self.print_check(app, "fail", "Not installed")
    
    def check_groq_integration(self):
        """Check Groq AI integration"""
        self.print_header("Groq AI Integration Check")
        
        try:
            groq_key = getattr(settings, 'GROQ_API_KEY', None)
            if groq_key:
                self.print_check("GROQ_API_KEY", "pass", f"Configured ({len(groq_key)} chars)")
                
                # Check if groq package is installed
                try:
                    import groq
                    self.print_check("Groq Package", "pass", f"Version {groq.__version__}")
                except ImportError:
                    self.print_check("Groq Package", "fail", "Not installed")
            else:
                self.print_check("GROQ_API_KEY", "warn", "Not configured (AI features disabled)")
        except Exception as e:
            self.print_check("Groq Integration", "fail", str(e))
    
    def print_summary(self):
        """Print summary of health checks"""
        self.print_header("Health Check Summary")
        
        total = len(self.passed) + len(self.failed) + len(self.warnings)
        
        print(f"\n✅ Passed:   {len(self.passed)}/{total}")
        print(f"❌ Failed:   {len(self.failed)}/{total}")
        print(f"⚠️  Warnings: {len(self.warnings)}/{total}")
        
        if self.failed:
            print("\n❌ Failed Checks:")
            for check in self.failed:
                print(f"   - {check}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for check in self.warnings:
                print(f"   - {check}")
        
        print("\n" + "=" * 60)
        
        if self.failed:
            print("❌ System is NOT ready for deployment!")
            print("   Please fix the failed checks above.")
            return False
        elif self.warnings:
            print("⚠️  System is ready with warnings.")
            print("   Review warnings before deploying to production.")
            return True
        else:
            print("✅ System is ready for deployment!")
            return True
    
    def run_all_checks(self):
        """Run all health checks"""
        print("\n" + "=" * 60)
        print("  🏥 IIMS System Health Check")
        print("  نظام فحص صحة IIMS")
        print("=" * 60)
        
        self.check_database()
        self.check_migrations()
        self.check_static_files()
        self.check_environment_variables()
        self.check_security_settings()
        self.check_installed_apps()
        self.check_groq_integration()
        
        return self.print_summary()


def main():
    """Main entry point"""
    checker = HealthChecker()
    success = checker.run_all_checks()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
