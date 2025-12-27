from django.core.management.base import BaseCommand
from intelligence.models import IntelligenceReport
from intelligence_agent.services import GroqClient
import time

class Command(BaseCommand):
    help = 'Force translates all reports to Arabic using the central service.'

    def handle(self, *args, **options):
        self.stdout.write("Starting Force Arabization of All Reports...")
        
        reports = IntelligenceReport.objects.all().order_by('-created_at')
        count = reports.count()
        self.stdout.write(f"Found {count} reports.")
        
        client = GroqClient()
        success_count = 0
        
        for i, report in enumerate(reports):
            # Feedback every 10 reports
            if i % 10 == 0:
                self.stdout.write(f"Processing {i}/{count}...")
                
            try:
                # Force translation even if partially done, or check internally
                # translate_report_obj checks if COMPLETED and translated_title exists
                # We can reset status if we want to FORCE re-translate
                # But for now, let's just ensure everything is translated
                
                result = client.translate_report_obj(report)
                if result:
                    success_count += 1
                
                # Sleep briefly to avoid rate limits if using real API
                if client.client: 
                    time.sleep(0.5)
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {report.id}: {e}"))
                
        self.stdout.write(self.style.SUCCESS(f"Finished. Successfully processed {success_count}/{count} reports."))
