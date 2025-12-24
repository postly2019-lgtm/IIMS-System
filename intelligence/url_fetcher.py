import requests
import re
from django.utils import timezone
from .models import Source, IntelligenceReport
from .analysis import ContentAnalyzer

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

class URLFetcher:
    def __init__(self):
        self.analyzer = ContentAnalyzer()
        # Ensure a generic source exists for manual fetches
        self.source, _ = Source.objects.get_or_create(
            name="Manual Web Fetch",
            defaults={
                'source_type': Source.SourceType.OTHER,
                'url': 'http://localhost',
                'reliability_score': 80,
                'is_active': True
            }
        )

    def fetch_and_process_urls(self, urls, query=None):
        """
        Fetches content from a list of URLs and creates IntelligenceReports.
        Returns a summary dict.
        """
        results = {
            'success': 0,
            'failed': 0,
            'errors': [],
            'reports': []
        }

        # Deduplicate URLs
        unique_urls = list(set(urls))[:50]  # Limit to 50 as requested

        for url in unique_urls:
            url = url.strip()
            if not url:
                continue
                
            # Check if already exists to avoid duplicates
            if IntelligenceReport.objects.filter(original_url=url).exists():
                results['errors'].append(f"Skipped (Duplicate): {url}")
                continue

            try:
                report = self._fetch_single_url(url, query)
                if report:
                    self.analyzer.analyze_report(report)
                    results['success'] += 1
                    results['reports'].append(report)
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Failed to parse: {url}")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error {url}: {str(e)}")

        return results

    def _fetch_single_url(self, url, query=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Auto-detect encoding
            if response.encoding is None:
                response.encoding = response.apparent_encoding

            html_content = response.text
            
            title = ""
            content = ""

            if HAS_BS4:
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract Title
                if soup.title:
                    title = soup.title.string
                else:
                    h1 = soup.find('h1')
                    title = h1.get_text() if h1 else url

                # Extract Content (simple heuristic: grab paragraphs)
                paragraphs = soup.find_all('p')
                content = "\n\n".join([p.get_text() for p in paragraphs])
                
                # Fallback if no paragraphs
                if not content:
                    content = soup.get_text()
            else:
                # Fallback Regex extraction
                title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
                title = title_match.group(1) if title_match else url
                
                # Strip tags for content
                content = re.sub(r'<[^>]+>', ' ', html_content)
                content = re.sub(r'\s+', ' ', content).strip()

            if not title:
                title = f"Report from {url}"
            
            # Truncate if necessary (though TextField usually handles large text)
            title = title.strip()[:200]

            # Extraction Logic if query is provided
            if query:
                query_matches = []
                lines = content.split('\n')
                for line in lines:
                    if query.lower() in line.lower():
                        query_matches.append(line.strip())
                
                if query_matches:
                    extraction_summary = f"** EXTRACTION RESULTS FOR '{query}' **\n"
                    extraction_summary += "\n- ".join(query_matches[:5]) # Top 5 matches
                    if len(query_matches) > 5:
                        extraction_summary += f"\n... and {len(query_matches)-5} more matches."
                    extraction_summary += "\n" + "="*40 + "\n\n"
                    
                    content = extraction_summary + content

            report = IntelligenceReport.objects.create(
                title=title,
                content=content,
                source=self.source,
                original_url=url,
                published_at=timezone.now(),
                classification=IntelligenceReport.Classification.UNCLASSIFIED,
                credibility_score=self.source.reliability_score
            )
            return report

        except Exception as e:
            raise e
