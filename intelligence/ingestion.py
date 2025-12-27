import feedparser
from django.utils import timezone
from .models import Source, IntelligenceReport
from .analysis import ContentAnalyzer
from datetime import datetime
from time import mktime

from bs4 import BeautifulSoup
from .utils.translation_engine import translator

class IngestionEngine:
    def __init__(self):
        self.analyzer = ContentAnalyzer()

    def clean_html(self, raw_html):
        """
        Removes HTML tags and returns clean text.
        """
        if not raw_html:
            return ""
        soup = BeautifulSoup(raw_html, "html.parser")
        return soup.get_text(separator="\n").strip()

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

        # --- Filter: Strictly Ignore Non-Intelligence Domains ---
        # If the source name or URL indicates non-relevant content (Health, Tech, Nature)
        # We skip it entirely to keep the system pure.
        ignored_keywords = [
            'nature.com', 'medical', 'health', 'clinic', 'science daily', 
            'techcrunch', 'gadget', 'sports', 'entertainment', 'celebrity',
            'nature journal', 'phys.org', 'new scientist'
        ]
        
        source_identity = (source.name + " " + source.url).lower()
        if any(keyword in source_identity for keyword in ignored_keywords):
            # Log skipped source if needed, but for now just return
            return

        feed = feedparser.parse(source.url)
        
        for entry in feed.entries:
            # --- Content Filter: Double Check Entry ---
            entry_text = (entry.title + " " + getattr(entry, 'link', '')).lower()
            if any(keyword in entry_text for keyword in ignored_keywords):
                continue
                
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

            raw_summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
            clean_content = self.clean_html(raw_summary)

            # --- Smart Dictionary Translation (Sovereign Engine) ---
            translated_title_val = translator.translate_text(entry.title)
            translated_content_val = translator.translate_text(clean_content)

            report = IntelligenceReport.objects.create(
                title=entry.title,
                content=clean_content,
                source=source,
                original_url=entry.link,
                published_at=published_time,
                credibility_score=credibility,
                translated_title=translated_title_val,
                translated_content=translated_content_val
            )
            
            # Analyze content immediately after ingestion
            self.analyzer.analyze_report(report)
        
        source.last_fetched_at = timezone.now()
        source.save()
