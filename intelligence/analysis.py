import re
from .models import IntelligenceReport, Entity, ClassificationRule, EntityExtractionPattern

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
        """
        Dynamic Entity Extraction based on Sovereign Patterns.
        """
        # Load all patterns (cached in practice, here direct DB for simplicity)
        patterns = EntityExtractionPattern.objects.all()
        
        for pattern in patterns:
            if pattern.pattern in text:
                 entity, created = Entity.objects.get_or_create(
                    name=pattern.pattern,
                    defaults={'entity_type': pattern.entity_type}
                )
                 report.entities.add(entity)

    def _classify_content(self, report, text):
        """
        Sovereign Classification Engine (SCE) - KSA Centric
        Implements strict logic for classification based on National Security parameters.
        """
        text_lower = text.lower()
        
        # Load rules ordered by weight (Highest priority first)
        rules = ClassificationRule.objects.filter(is_active=True).order_by('-weight')
        
        matched_rule = None
        
        for rule in rules:
            # Check keywords (OR logic) - Triggering keywords
            keywords = [k.strip().lower() for k in rule.keywords.split(',') if k.strip()]
            has_keyword = any(k in text_lower for k in keywords)
            
            if not has_keyword:
                continue
                
            # Check required keywords (AND logic) - Contextual keywords
            # If required_keywords is present, AT LEAST ONE of them must be in text
            if rule.required_keywords:
                req_keywords = [k.strip().lower() for k in rule.required_keywords.split(',') if k.strip()]
                has_required = any(k in text_lower for k in req_keywords)
                if not has_required:
                    continue
            
            # If we are here, rule matches
            matched_rule = rule
            break # Stop at first high-weight match
            
        if matched_rule:
            report.classification = matched_rule.classification
            report.topic = matched_rule.topic
            report.severity = matched_rule.severity
            
            # Dynamic Credibility Adjustment for Critical Threats
            if matched_rule.severity == 'CRITICAL':
                report.credibility_score = 100
            elif matched_rule.severity == 'HIGH':
                report.credibility_score = max(report.credibility_score, 90)
                
        else:
            report.classification = IntelligenceReport.Classification.UNCLASSIFIED
            report.topic = 'GENERAL_INTEL'
            
        report.save()
