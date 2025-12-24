from django.core.management.base import BaseCommand
from intelligence.ingestion import IngestionEngine
from intelligence.models import Source

class Command(BaseCommand):
    help = 'Ingest news from active sources'

    def handle(self, *args, **options):
        # Seed some default sources if none exist
        if not Source.objects.exists():
            self.stdout.write("Seeding default sources...")
            Source.objects.create(
                name='Al Jazeera (Arabic)',
                url='https://www.aljazeera.net/aljazeerarss/a7c186be-1baa-4bd4-9d80-a84db769f779/73d0e1b4-532f-45ef-b135-bf4aefee8869',
                source_type=Source.SourceType.RSS,
                reliability_score=85
            )
            Source.objects.create(
                name='BBC Arabic',
                url='https://feeds.bbci.co.uk/arabic/rss.xml',
                source_type=Source.SourceType.RSS,
                reliability_score=90
            )
            Source.objects.create(
                name='Sky News Arabia',
                url='https://www.skynewsarabia.com/web/rss',
                source_type=Source.SourceType.RSS,
                reliability_score=80
            )

        self.stdout.write("Starting ingestion...")
        engine = IngestionEngine()
        results = engine.fetch_all()
        self.stdout.write(self.style.SUCCESS(f"Ingestion Complete. Success: {results['success']}, Failed: {results['failed']}"))
