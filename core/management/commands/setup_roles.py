from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from intelligence.models import IntelligenceReport

class Command(BaseCommand):
    help = 'Setup system roles and permissions'

    def handle(self, *args, **options):
        # Create Groups
        analyst_group, created = Group.objects.get_or_create(name='Analyst')
        browser_group, created = Group.objects.get_or_create(name='Browser')

        # Get Permissions
        report_ct = ContentType.objects.get_for_model(IntelligenceReport)
        view_report = Permission.objects.get(codename='view_intelligencereport', content_type=report_ct)
        add_report = Permission.objects.get(codename='add_intelligencereport', content_type=report_ct)
        change_report = Permission.objects.get(codename='change_intelligencereport', content_type=report_ct)

        # Assign Permissions to Analyst
        analyst_group.permissions.add(view_report, add_report, change_report)
        self.stdout.write(self.style.SUCCESS('Updated Analyst Group Permissions'))

        # Assign Permissions to Browser
        browser_group.permissions.add(view_report)
        self.stdout.write(self.style.SUCCESS('Updated Browser Group Permissions'))
