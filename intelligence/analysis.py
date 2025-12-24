import re
from .models import IntelligenceReport, Entity

class ContentAnalyzer:
    def analyze_report(self, report: IntelligenceReport):
        """
        Analyzes the report content to extract entities and update metadata.
        """
        text = f"{report.title} {report.content}"
        
        # 1. Entity Extraction
        self._extract_entities(report, text)
        
        # 2. Cross-Referencing & Linking
        self._find_related_reports(report)

        # 3. Dynamic Credibility Scoring
        self._update_credibility(report)
        
        # 4. Classification
        self._classify_content(report, text)

    def _find_related_reports(self, report):
        """
        Finds related reports based on title similarity and shared entities.
        """
        # Get recent reports (e.g., last 48 hours) excluding self
        # For simplicity, we'll check last 50 reports
        candidates = IntelligenceReport.objects.exclude(id=report.id).order_by('-published_at')[:50]
        
        report_tokens = set(report.title.split())
        
        for candidate in candidates:
            # Check Title Similarity (Jaccard Index)
            candidate_tokens = set(candidate.title.split())
            intersection = report_tokens.intersection(candidate_tokens)
            union = report_tokens.union(candidate_tokens)
            
            if not union:
                continue
                
            similarity = len(intersection) / len(union)
            
            # Check Shared Entities
            shared_entities = report.entities.all() & candidate.entities.all()
            
            # If significant similarity or shared entities found
            if similarity > 0.1 or shared_entities.exists(): # Low threshold for demo
                report.related_reports.add(candidate)

    def _update_credibility(self, report):
        """
        Updates credibility score based on source reliability and cross-references.
        """
        base_score = report.source.reliability_score
        
        # Corroboration Bonus
        # Check how many distinct sources have reported similar stories
        related_sources = set()
        for related in report.related_reports.all():
            related_sources.add(related.source.id)
            
        # Add 5 points for each corroborating source (excluding own source)
        if report.source.id in related_sources:
            related_sources.remove(report.source.id)
            
        bonus = len(related_sources) * 5
        
        final_score = min(100, base_score + bonus)
        report.credibility_score = final_score
        report.save()

    def _extract_entities(self, report, text):
        # Example: predefined watch list or patterns
        # For demo purposes, we'll look for common keywords and create entities
        
        common_entities = {
            'الرئيس': Entity.EntityType.PERSON,
            'الوزير': Entity.EntityType.PERSON,
            'الأمم المتحدة': Entity.EntityType.ORGANIZATION,
            'مجلس الأمن': Entity.EntityType.ORGANIZATION,
            'واشنطن': Entity.EntityType.LOCATION,
            'الرياض': Entity.EntityType.LOCATION,
            'القاهرة': Entity.EntityType.LOCATION,
            'غزة': Entity.EntityType.LOCATION,
            'كييف': Entity.EntityType.LOCATION,
            'موسكو': Entity.EntityType.LOCATION,
        }

        for keyword, entity_type in common_entities.items():
            if keyword in text:
                # Get or Create Entity
                entity, created = Entity.objects.get_or_create(
                    name=keyword,
                    defaults={'entity_type': entity_type}
                )
                report.entities.add(entity)

    def _classify_content(self, report, text):
        # Simple keyword-based sensitivity classification
        urgent_keywords = ['عاجل', 'انفجار', 'هجوم', 'مقتل', 'اغتيال']
        
        score = 0
        for word in urgent_keywords:
            if word in text:
                score += 20
        
        # Update credibility/classification based on content analysis
        if score > 50:
            report.classification = IntelligenceReport.Classification.SECRET
        elif score > 20:
            report.classification = IntelligenceReport.Classification.CONFIDENTIAL
        
        report.save()
