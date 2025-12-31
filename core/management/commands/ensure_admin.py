from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Ensures an admin user exists with credentials from environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME') or os.environ.get('DJANGO_SUPERUSER_USERNAME') or 'admin'
        email = os.environ.get('ADMIN_EMAIL') or os.environ.get('DJANGO_SUPERUSER_EMAIL') or 'admin@iims.local'
        password = os.environ.get('ADMIN_PASSWORD') or os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        job_number = os.environ.get('ADMIN_JOB_NUMBER') or 'ADMIN-001'
        rank = os.environ.get('ADMIN_RANK') or 'MIL'
        first_name = os.environ.get('ADMIN_FIRST_NAME') or 'System'
        last_name = os.environ.get('ADMIN_LAST_NAME') or 'Administrator'

        if not password:
            self.stdout.write(self.style.WARNING("ADMIN_PASSWORD not set in environment. Skipping admin creation."))
            return

        try:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})

            desired_job_number = job_number
            if User.objects.exclude(pk=user.pk).filter(job_number=desired_job_number).exists():
                desired_job_number = f"{job_number}-{username}".upper()
            
            if created:
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.role = 'ADMIN'
                user.rank = rank
                user.first_name = first_name
                user.last_name = last_name
                if not getattr(user, 'job_number', None):
                    user.job_number = desired_job_number
                if hasattr(user, 'requires_smart_card'):
                    user.requires_smart_card = False
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully created admin user: {username}"))
            else:
                # Update existing user to ensure access
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.role = 'ADMIN'
                user.rank = rank
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                if not getattr(user, 'job_number', None):
                    user.job_number = desired_job_number
                if hasattr(user, 'requires_smart_card'):
                    user.requires_smart_card = False
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully updated admin user password: {username}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error managing admin user: {str(e)}"))
