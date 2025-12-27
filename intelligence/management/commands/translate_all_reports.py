from django.core.management.base import BaseCommand
from intelligence.models import IntelligenceReport
from intelligence_agent.services import GroqClient
import time
import os

class Command(BaseCommand):
    help = 'Translate all English reports to Arabic'

    def handle(self, *args, **kwargs):
        # Create directory if not exists (standard Django command structure)
        
        all_reports = IntelligenceReport.objects.all()
        client = GroqClient()
        
        self.stdout.write(f"Found {all_reports.count()} reports to check...")
        
        for report in all_reports:
            # Simple check if arabic
            if report.title and any("\u0600" <= c <= "\u06FF" for c in report.title):
                self.stdout.write(self.style.SUCCESS(f"Skipping {report.id} (Already Arabic)"))
                continue
                
            self.stdout.write(f"Translating Report {report.id}...")
            
            try:
                # Translate Title
                title_prompt = f"Translate the following intelligence report title to professional Arabic (Military/Intel style). Return ONLY the translated text:\n\n{report.title}"
                # Using lower level access if needed, but chat_completion should work if API key is set
                if not os.environ.get("GROQ_API_KEY"):
                     self.stdout.write(self.style.ERROR("GROQ_API_KEY not found in environment"))
                     return

                translated_title = client.chat_completion(title_prompt)
                
                # Translate Content
                content_prompt = f"Translate the following intelligence report content to professional Arabic (Military/Intel style). Maintain all details. Return ONLY the translated text:\n\n{report.content}"
                translated_content = client.chat_completion(content_prompt)
                
                if translated_title:
                    report.title = translated_title
                if translated_content:
                    report.content = translated_content
                
                report.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully translated Report {report.id}"))
                time.sleep(1) # Rate limit
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to translate {report.id}: {e}"))
