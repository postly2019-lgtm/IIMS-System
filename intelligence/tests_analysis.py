from django.test import TestCase
from .models import IntelligenceReport, Source, Entity
from .analysis import ContentAnalyzer

class AnalysisTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(name='Test Source', reliability_score=80)
        self.analyzer = ContentAnalyzer()

    def test_entity_extraction(self):
        # Create a report with keywords
        report = IntelligenceReport.objects.create(
            title="اجتماع عاجل في واشنطن",
            content="صرح الرئيس بأن الأمم المتحدة ستعقد جلسة طارئة.",
            source=self.source,
            original_url="http://test.com/1",
            credibility_score=80
        )
        
        self.analyzer.analyze_report(report)
        
        # Verify Entities
        # "واشنطن" -> Location
        # "الرئيس" -> Person
        # "الأمم المتحدة" -> Organization
        self.assertTrue(report.entities.filter(name="واشنطن", entity_type=Entity.EntityType.LOCATION).exists())
        self.assertTrue(report.entities.filter(name="الرئيس", entity_type=Entity.EntityType.PERSON).exists())
        self.assertTrue(report.entities.filter(name="الأمم المتحدة", entity_type=Entity.EntityType.ORGANIZATION).exists())
        print("\n[TEST] Entity Extraction Verified.")

    def test_classification_logic(self):
        report = IntelligenceReport.objects.create(
            title="انفجار في العاصمة",
            content="أنباء عن هجوم ومقتل عدد من الأشخاص.",
            source=self.source,
            original_url="http://test.com/2",
            credibility_score=80
        )
        
        self.analyzer.analyze_report(report)
        
        # Should be upgraded to SECRET or CONFIDENTIAL based on keywords "انفجار", "هجوم", "مقتل"
        # Score: 20+20+20 = 60 -> SECRET
        self.assertEqual(report.classification, IntelligenceReport.Classification.SECRET)
        print("\n[TEST] Content Classification Verified.")
