from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@iims.local')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin@12345')

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' already exists.")
        else:
            self.stdout.write(f"Creating superuser '{username}'...")
            try:
                User.objects.create_superuser(
                    username=username, 
                    email=email, 
                    password=password,
                    job_number='ADMIN-001',
                    rank='MIL',
                    first_name='System',
                    last_name='Administrator'
                )
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))
                self.stdout.write(self.style.SUCCESS(f"Password: {password}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating superuser: {str(e)}"))
