from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Initialize the system with the default security user'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'sec'
        password = 'Aa159632@'
        
        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Creating user {username}...'))
            user = User.objects.create_superuser(
                username=username,
                password=password,
                email='sec@iims.local',
                first_name='مدير',
                last_name='النظام',
                job_number='SEC-001',
                rank='MIL'
            )
            self.stdout.write(self.style.SUCCESS(f'User {username} created successfully.'))
            self.stdout.write(self.style.SUCCESS(f'Password set to: {password}'))
            
            # Verify QR Code generation
            if user.qr_code:
                self.stdout.write(self.style.SUCCESS(f'QR Code generated at: {user.qr_code.path}'))
                self.stdout.write(self.style.SUCCESS(f'Card View URL: http://127.0.0.1:8000/card/{username}/'))
            else:
                self.stdout.write(self.style.ERROR('QR Code was not generated.'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists.'))
