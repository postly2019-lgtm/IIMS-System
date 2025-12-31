from django.core.management.base import BaseCommand
from intelligence.models import IntelligenceReport
from intelligence_agent.services import GroqClient
import time

class Command(BaseCommand):
    help = 'Backfills Arabic translations for reports missing title_ar'

    def handle(self, *args, **options):
        reports = IntelligenceReport.objects.filter(title_ar__isnull=True) | IntelligenceReport.objects.filter(title_ar='')
        total = reports.count()
        self.stdout.write(f"Found {total} reports needing translation...")
        
        client = None
        try:
            client = GroqClient()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to init GroqClient: {e}"))
            return

        count = 0
        for report in reports:
            self.stdout.write(f"Translating report {report.id}: {report.title[:30]}...")
            try:
                # Translate Title
                title_ar = client.translate_with_chunking(report.title, is_title=True)
                
                # Translate Content (if exists)
                content_ar = ""
                if report.content:
                    content_ar = client.translate_with_chunking(report.content)
                
                if title_ar:
                    report.title_ar = title_ar
                    report.content_ar = content_ar
                    # Also update legacy fields for compatibility
                    report.translated_title = title_ar
                    report.translated_content = content_ar
                    report.save()
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Translated {report.id}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped {report.id} (Translation returned empty)"))
                
                # Rate limit to avoid hitting API limits too hard during backfill
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {report.id}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"Completed. Translated {count}/{total} reports."))
