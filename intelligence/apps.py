from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command
import sys

def seed_data_on_migrate(sender, **kwargs):
    """
    Auto-seed sources and prompts after migration if database is empty.
    Crucial for ephemeral deployments (Railway/Heroku with SQLite).
    """
    if 'test' in sys.argv:
        return

    from intelligence.models import Source
    from intelligence_agent.models import AgentInstruction
    
    # Check Sources
    if not Source.objects.exists():
        print("🌱 Database empty. Auto-seeding sources...")
        try:
            call_command('seed_sources')
        except Exception as e:
            print(f"⚠️ Seeding failed: {e}")

    # Check Reports (Ingest if sources exist but no reports)
    from intelligence.models import IntelligenceReport
    if Source.objects.exists() and not IntelligenceReport.objects.exists():
        print("📰 Sources found but no reports. Auto-ingesting news...")
        try:
            call_command('ingest_news')
        except Exception as e:
            print(f"⚠️ Ingestion failed: {e}")

    # Check Agent Prompts
    if not AgentInstruction.objects.exists():
        print("🤖 No agent instructions found. Auto-seeding OSINT prompt...")
        try:
            call_command('update_prompts')
        except Exception as e:
            print(f"⚠️ Prompt update failed: {e}")

class IntelligenceConfig(AppConfig):
    default = True
    name = 'intelligence'

    def ready(self):
        post_migrate.connect(seed_data_on_migrate, sender=self)
