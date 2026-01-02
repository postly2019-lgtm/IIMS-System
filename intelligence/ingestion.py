import feedparser
import sys
from django.utils import timezone
from .models import Source, IntelligenceReport
from .analysis import ContentAnalyzer
from datetime import datetime
from time import mktime

from bs4 import BeautifulSoup
from .utils.translation_engine import translator
from intelligence_agent.services import GroqClient

class IngestionEngine:
    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self._ignored_keywords_cache = None
        self.groq_client = None
        if 'test' not in sys.argv:
            self.groq_client = GroqClient()

    def clean_html(self, raw_html):
        """
        Removes HTML tags, normalizes whitespace, and fixes encoding issues.
        """
        if not raw_html:
            return ""
        
        # 1. Parse HTML
        soup = BeautifulSoup(raw_html, "html.parser")
        
        # 2. Extract Text with smart separator
        text = soup.get_text(separator=" ")
        
        # 3. Normalize Whitespace (remove excessive newlines/tabs)
        import re
        import unicodedata
        
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        
        # 4. Normalize Unicode (NFKC handles compatibility characters)
        text = unicodedata.normalize('NFKC', text)
        
        # 5. Remove common garbage symbols often found in RSS
        text = text.replace('â€™', "'").replace('â€œ', '"').replace('â€', '"')
        text = text.replace('&nbsp;', ' ')
        
        return text.strip()

    def _get_ignored_keywords(self):
        """Loads ignored keywords from DB (Sovereign Configuration)"""
        if self._ignored_keywords_cache is None:
            try:
                from .models import IgnoredSource
                # Fetch and lowercase
                keywords = IgnoredSource.objects.filter(is_active=True).values_list('keyword', flat=True)
                self._ignored_keywords_cache = [k.lower() for k in keywords]
            except Exception as e:
                print(f"Error loading ignored sources: {e}")
                # Fallback to empty if DB fails
                self._ignored_keywords_cache = []
        return self._ignored_keywords_cache

    def fetch_all(self):
        sources = Source.objects.filter(is_active=True, source_type=Source.SourceType.RSS)
        results = {'success': 0, 'failed': 0}
        
        # Refresh cache once per batch run
        self._ignored_keywords_cache = None 
        
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

        ignored_keywords = self._get_ignored_keywords()
        
        # --- Filter: Strictly Ignore Non-Intelligence Domains ---
        source_identity = (source.name + " " + source.url).lower()
        if any(keyword in source_identity for keyword in ignored_keywords):
            # Log skipped source if needed, but for now just return
            return

        # --- Content Validation (Sovereign Guard) ---
        # 1. Check for valid URL scheme
        if not source.url.startswith(('http://', 'https://')):
             print(f"Skipping invalid URL scheme: {source.url}")
             return

        try:
            feed = feedparser.parse(source.url)
        except Exception as e:
            print(f"Feed parsing error for {source.name}: {e}")
            return
        
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

            # --- Sovereign AI Translation (Groq) ---
            # Priority: LLM -> Dictionary Fallback -> Original
            title_ar_val = None
            content_ar_val = None

            if self.groq_client:
                # 1. Title Translation
                title_ar_val = self.groq_client.translate_with_chunking(entry.title, is_title=True)
                
                # 2. Content Translation (Chunked)
                if clean_content:
                    content_ar_val = self.groq_client.translate_with_chunking(clean_content)

            # Fallback to Dictionary if LLM fails or is offline
            if not title_ar_val:
                title_ar_val = translator.translate_text(entry.title)
            if not content_ar_val:
                content_ar_val = translator.translate_text(clean_content)

            report = IntelligenceReport.objects.create(
                title=entry.title,
                content=clean_content,
                source=source,
                original_url=entry.link,
                published_at=published_time,
                credibility_score=credibility,
                # Store in Arabic Fields (Mission D)
                title_ar=title_ar_val,
                content_ar=content_ar_val,
                # Keep legacy fields synced for now
                translated_title=title_ar_val,
                translated_content=content_ar_val,
                processing_status='COMPLETED' if title_ar_val else 'PENDING'
            )
            
            # Analyze content immediately after ingestion
            self.analyzer.analyze_report(report)
        
        source.last_fetched_at = timezone.now()
        source.save()
