import feedparser
from django.utils import timezone
from .models import Source, IntelligenceReport
from .analysis import ContentAnalyzer
from datetime import datetime
from time import mktime

class IngestionEngine:
    def __init__(self):
        self.analyzer = ContentAnalyzer()

    def fetch_all(self):
        sources = Source.objects.filter(is_active=True, source_type=Source.SourceType.RSS)
        results = {'success': 0, 'failed': 0}
        
        for source in sources:
            try:
                self.process_rss_source(source)
                results['success'] += 1
            except Exception as e:
                print(f"Error fetching {source.name}: {e}")
                results['failed'] += 1
        return results

    def process_rss_source(self, source):
        if not source.url:
            return

        feed = feedparser.parse(source.url)
        
        for entry in feed.entries:
            # Check if exists
            if IntelligenceReport.objects.filter(original_url=entry.link).exists():
                continue

            published_time = timezone.now()
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_time = datetime.fromtimestamp(mktime(entry.published_parsed))
                published_time = timezone.make_aware(published_time)

            # Basic Reliability Logic:
            # Source Reliability (50%) + Freshness (20%) + ...
            # For now, inherit source reliability as base credibility
            credibility = source.reliability_score

            report = IntelligenceReport.objects.create(
                title=entry.title,
                content=getattr(entry, 'summary', '') or getattr(entry, 'description', ''),
                source=source,
                original_url=entry.link,
                published_at=published_time,
                credibility_score=credibility
            )
            
            # Analyze content immediately after ingestion
            self.analyzer.analyze_report(report)
        
        source.last_fetched_at = timezone.now()
        source.save()
