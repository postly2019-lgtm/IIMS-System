from django.test import TestCase
from .models import Source, IntelligenceReport
from .ingestion import IngestionEngine
from unittest.mock import MagicMock, patch

class IngestionTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name='Test Source',
            url='http://test.com/rss',
            source_type=Source.SourceType.RSS,
            reliability_score=80
        )

    @patch('feedparser.parse')
    def test_rss_ingestion(self, mock_parse):
        # Mock Feedparser response
        mock_feed = MagicMock()
        mock_entry = MagicMock()
        mock_entry.title = "Test News Title"
        mock_entry.summary = "Test Content Body"
        mock_entry.link = "http://test.com/article/1"
        mock_entry.published_parsed = None # Use current time
        
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed

        # Run Ingestion
        engine = IngestionEngine()
        engine.process_rss_source(self.source)

        # Verify
        self.assertEqual(IntelligenceReport.objects.count(), 1)
        report = IntelligenceReport.objects.first()
        self.assertEqual(report.title, "Test News Title")
        self.assertEqual(report.credibility_score, 80) # Should inherit source score
        print("\n[TEST] Ingestion Engine Logic Verified.")
