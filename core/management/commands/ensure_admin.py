from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Ensures an admin user exists with credentials from environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD')

        if not password:
            self.stdout.write(self.style.WARNING("ADMIN_PASSWORD not set in environment. Skipping admin creation."))
            return

        try:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            
            if created:
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.role = 'ADMIN'  # Ensure role is set for custom user model
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully created admin user: {username}"))
            else:
                # Update existing user to ensure access
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.role = 'ADMIN'
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully updated admin user password: {username}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error managing admin user: {str(e)}"))
