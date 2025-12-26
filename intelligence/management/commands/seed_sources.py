from django.core.management.base import BaseCommand
from intelligence.models import Source

class Command(BaseCommand):
    help = 'Seeds the database with high-quality intelligence sources'

    def handle(self, *args, **kwargs):
        sources = [
            # --- Arabic News (Tier 1) ---
            {
                "name": "قناة العربية - الأخبار العاجلة",
                "url": "https://www.alarabiya.net/.mrss/ar/breaking-news.xml",
                "type": Source.SourceType.RSS,
                "category": "News - Arabic",
                "reliability": 90
            },
            {
                "name": "الجزيرة - الأخبار الرئيسية",
                "url": "https://www.aljazeera.net/aljazeerarss/a7c186be-1baa-4bd4-9d80-a84db769f779/73d0e1b4-532f-45ef-b135-bf70c53e4086",
                "type": Source.SourceType.RSS,
                "category": "News - Arabic",
                "reliability": 85
            },
            {
                "name": "سكاي نيوز عربية",
                "url": "https://www.skynewsarabia.com/web/rss",
                "type": Source.SourceType.RSS,
                "category": "News - Arabic",
                "reliability": 88
            },
            {
                "name": "BBC News - عربي",
                "url": "https://feeds.bbci.co.uk/arabic/rss.xml",
                "type": Source.SourceType.RSS,
                "category": "News - Arabic",
                "reliability": 95
            },
            {
                "name": "CNN بالعربية",
                "url": "https://arabic.cnn.com/api/v1/rss/headlines/index.xml",
                "type": Source.SourceType.RSS,
                "category": "News - Arabic",
                "reliability": 90
            },

            # --- Global Intelligence & Military (Tier 1) ---
            {
                "name": "Defense One (Global Defense)",
                "url": "https://www.defenseone.com/rss/all/",
                "type": Source.SourceType.RSS,
                "category": "Military & Defense",
                "reliability": 92
            },
            {
                "name": "Breaking Defense",
                "url": "https://breakingdefense.com/feed/",
                "type": Source.SourceType.RSS,
                "category": "Military & Defense",
                "reliability": 88
            },
            {
                "name": "Jane's 360 (Defence)",
                "url": "https://www.janes.com/feeds/news",
                "type": Source.SourceType.RSS,
                "category": "Military & Defense",
                "reliability": 95
            },
            {
                "name": "Global Security Newswire",
                "url": "https://www.nti.org/gsn/rss/",
                "type": Source.SourceType.RSS,
                "category": "Intelligence",
                "reliability": 90
            },
             {
                "name": "Military.com News",
                "url": "http://feeds.feedburner.com/Military-Headlines-Content",
                "type": Source.SourceType.RSS,
                "category": "Military & Defense",
                "reliability": 85
            },

            # --- Global News Agencies (Tier 1) ---
            {
                "name": "Reuters - World News",
                "url": "https://www.reutersagency.com/feed/?best-topics=world&post_type=best",
                "type": Source.SourceType.RSS,
                "category": "Global News",
                "reliability": 98
            },
            {
                "name": "Associated Press (AP)",
                "url": "https://apnews.com/apf-topnews",
                "type": Source.SourceType.RSS,
                "category": "Global News",
                "reliability": 98
            },
            {
                "name": "The Guardian - World",
                "url": "https://www.theguardian.com/world/rss",
                "type": Source.SourceType.RSS,
                "category": "Global News",
                "reliability": 90
            },

            # --- Science & Technology ---
            {
                "name": "ScienceDaily - Top Science",
                "url": "https://www.sciencedaily.com/rss/top/science.xml",
                "type": Source.SourceType.RSS,
                "category": "Science",
                "reliability": 95
            },
            {
                "name": "Nature Journal",
                "url": "http://www.nature.com/nature/current_issue/rss/",
                "type": Source.SourceType.RSS,
                "category": "Science",
                "reliability": 100
            },
            {
                "name": "Scientific American",
                "url": "http://rss.sciam.com/ScientificAmerican-Global",
                "type": Source.SourceType.RSS,
                "category": "Science",
                "reliability": 95
            },
            {
                "name": "MIT Technology Review",
                "url": "https://www.technologyreview.com/feed/",
                "type": Source.SourceType.RSS,
                "category": "Technology",
                "reliability": 92
            },
            {
                "name": "Wired - Security",
                "url": "https://www.wired.com/feed/category/security/latest/rss",
                "type": Source.SourceType.RSS,
                "category": "Technology",
                "reliability": 88
            },
            {
                "name": "NASA Breaking News",
                "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
                "type": Source.SourceType.RSS,
                "category": "Science",
                "reliability": 100
            },

            # --- Cybersecurity & Cyberwarfare ---
            {
                "name": "The Hacker News",
                "url": "https://feeds.feedburner.com/TheHackersNews",
                "type": Source.SourceType.RSS,
                "category": "Cybersecurity",
                "reliability": 90
            },
            {
                "name": "Krebs on Security",
                "url": "https://krebsonsecurity.com/feed/",
                "type": Source.SourceType.RSS,
                "category": "Cybersecurity",
                "reliability": 95
            },
            {
                "name": "Threatpost",
                "url": "https://threatpost.com/feed/",
                "type": Source.SourceType.RSS,
                "category": "Cybersecurity",
                "reliability": 88
            },
            {
                "name": "Dark Reading",
                "url": "https://www.darkreading.com/rss.xml",
                "type": Source.SourceType.RSS,
                "category": "Cybersecurity",
                "reliability": 85
            },
            
            # --- Economy & Geopolitics ---
            {
                "name": "The Economist - World",
                "url": "https://www.economist.com/international/rss.xml",
                "type": Source.SourceType.RSS,
                "category": "Economy & Politics",
                "reliability": 92
            },
            {
                "name": "Bloomberg Politics",
                "url": "https://feeds.bloomberg.com/politics/news.xml",
                "type": Source.SourceType.RSS,
                "category": "Economy & Politics",
                "reliability": 90
            },
            {
                "name": "Financial Times - World",
                "url": "https://www.ft.com/?format=rss",
                "type": Source.SourceType.RSS,
                "category": "Economy & Politics",
                "reliability": 92
            },
            {
                "name": "CNBC International",
                "url": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
                "type": Source.SourceType.RSS,
                "category": "Economy & Politics",
                "reliability": 88
            },

             # --- Regional / Middle East Specific ---
            {
                "name": "Asharq Al-Awsat (English)",
                "url": "https://english.aawsat.com/home/rss",
                "type": Source.SourceType.RSS,
                "category": "Regional",
                "reliability": 85
            },
            {
                "name": "The Jerusalem Post",
                "url": "https://www.jpost.com/rss/rssfeedsheadlines.aspx",
                "type": Source.SourceType.RSS,
                "category": "Regional",
                "reliability": 80
            },
            {
                "name": "Tehran Times",
                "url": "https://www.tehrantimes.com/rss",
                "type": Source.SourceType.RSS,
                "category": "Regional",
                "reliability": 70
            },

            # --- Health, Disease & Epidemics (New) ---
            {
                "name": "World Health Organization (WHO) - News",
                "url": "https://www.who.int/feeds/entity/news/en/rss.xml",
                "type": Source.SourceType.RSS,
                "category": "Health & Diseases",
                "reliability": 100
            },
            {
                "name": "CDC - Outbreaks",
                "url": "https://tools.cdc.gov/api/v2/resources/media/132608.rss",
                "type": Source.SourceType.RSS,
                "category": "Health & Diseases",
                "reliability": 100
            },
            {
                "name": "The Lancet - Global Health",
                "url": "https://www.thelancet.com/rssfeed/langlo_current.xml",
                "type": Source.SourceType.RSS,
                "category": "Health & Diseases",
                "reliability": 98
            },
            {
                "name": "CIDRAP (Infectious Disease Research)",
                "url": "https://www.cidrap.umn.edu/rss/cidrap_news.xml",
                "type": Source.SourceType.RSS,
                "category": "Health & Diseases",
                "reliability": 95
            },
            {
                "name": "Medical News Today",
                "url": "https://www.medicalnewstoday.com/feed",
                "type": Source.SourceType.RSS,
                "category": "Health & Diseases",
                "reliability": 85
            },
            {
                "name": "NIH (National Institutes of Health)",
                "url": "https://www.nih.gov/news-events/feed.xml",
                "type": Source.SourceType.RSS,
                "category": "Health & Diseases",
                "reliability": 98
            },
            {
                "name": "European Centre for Disease Prevention and Control (ECDC)",
                "url": "https://www.ecdc.europa.eu/en/rss/feeds/all/rss.xml",
                "type": Source.SourceType.RSS,
                "category": "Health & Diseases",
                "reliability": 95
            },
        ]

        count = 0
        for src in sources:
            obj, created = Source.objects.get_or_create(
                url=src['url'],
                defaults={
                    'name': src['name'],
                    'source_type': src['type'],
                    'category': src['category'],
                    'reliability_score': src['reliability'],
                    'is_active': True
                }
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {src['name']}"))
            else:
                self.stdout.write(f"Skipped (Exists): {src['name']}")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new sources.'))
