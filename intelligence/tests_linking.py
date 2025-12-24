from django.test import TestCase
from .models import IntelligenceReport, Source, Entity
from .analysis import ContentAnalyzer

class LinkingTest(TestCase):
    def setUp(self):
        self.source1 = Source.objects.create(name='Source 1', reliability_score=50)
        self.source2 = Source.objects.create(name='Source 2', reliability_score=50)
        self.analyzer = ContentAnalyzer()

    def test_cross_referencing(self):
        # Create Report 1
        r1 = IntelligenceReport.objects.create(
            title="انفجار كبير في العاصمة",
            content="وقع انفجار ضخم وسط العاصمة اليوم.",
            source=self.source1,
            credibility_score=50
        )
        self.analyzer.analyze_report(r1)

        # Create Report 2 (Similar Title, Different Source)
        r2 = IntelligenceReport.objects.create(
            title="أنباء عن انفجار في العاصمة",
            content="تفاصيل أولية عن الانفجار الذي هز العاصمة.",
            source=self.source2,
            credibility_score=50
        )
        
        # Analyze R2 -> Should link to R1
        self.analyzer.analyze_report(r2)
        
        # Verify Link (Symmetrical)
        self.assertTrue(r2.related_reports.filter(id=r1.id).exists())
        self.assertTrue(r1.related_reports.filter(id=r2.id).exists())
        print("\n[TEST] Cross-Referencing Verified.")

    def test_credibility_boost(self):
        # Report 1
        r1 = IntelligenceReport.objects.create(title="Title A", content="Content A", source=self.source1, credibility_score=50)
        self.analyzer.analyze_report(r1)
        
        # Report 2 (Similar)
        r2 = IntelligenceReport.objects.create(title="Title A", content="Content A", source=self.source2, credibility_score=50)
        self.analyzer.analyze_report(r2)
        
        # Check if credibility increased
        # R2 should have found R1. Base 50 + 5 (1 related source) = 55
        r2.refresh_from_db()
        self.assertEqual(r2.credibility_score, 55)
        print("\n[TEST] Credibility Boost Verified.")
