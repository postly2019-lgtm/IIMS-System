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
        """
        Sovereign Classification Engine (SCE) - KSA Centric
        Implements strict logic for classification based on National Security parameters.
        """
        text_lower = text.lower()
        
        # --- KEYWORD GROUPS ---
        
        # 1. KSA Identifiers
        ksa_keywords = ['saudi', 'ksa', 'riyadh', 'kingdom', 'bin salman', 'السعودية', 'المملكة', 'الرياض', 'سلمان', 'ولي العهد']
        
        # 2. Negative/Threat Indicators
        threat_keywords = [
            'attack', 'violation', 'criticism', 'failure', 'human rights', 'khashoggi', 'yemen war', 
            'هجوم', 'انتهاك', 'انتقاد', 'فشل', 'حقوق انسان', 'حرب اليمن', 'تدخل', 'sanctions', 'عقوبات'
        ]
        
        # 3. Armed Forces
        military_forces_keywords = ['armed forces', 'royal guard', 'air force', 'navy', 'القوات المسلحة', 'الحرس الملكي', 'الجيش', 'القوات الجوية']
        
        # 4. Internal/Reputation
        internal_keywords = ['economy', 'oil', 'aramco', 'inflation', 'unemployment', 'debt', 'اقتصاد', 'نفط', 'أرامكو', 'تضخم', 'بطالة', 'ديون']
        
        # 5. Achievements/Vision
        vision_keywords = ['vision 2030', 'neom', 'project', 'launch', 'achievement', 'growth', 'رؤية 2030', 'نيوم', 'مشروع', 'إطلاق', 'إنجاز', 'نمو', 'تطور']
        
        # 6. Regional Neighbors (Security Context)
        neighbors = ['yemen', 'iran', 'iraq', 'jordan', 'kuwait', 'bahrain', 'qatar', 'uae', 'oman', 'houthi', 
                    'اليمن', 'إيران', 'العراق', 'الأردن', 'الكويت', 'البحرين', 'قطر', 'الإمارات', 'عمان', 'حوثي']
        
        # 7. Critical Military Events (General)
        critical_events = [
            'war', 'explosion', 'bomb', 'killing', 'killed', 'withdrawal', 'disarmament', 'weapon', 'missile', 'drone', 'terror',
            'حرب', 'انفجار', 'قنبلة', 'مقتل', 'قتل', 'انسحاب', 'نزع سلاح', 'سلاح', 'صاروخ', 'طائرة مسيرة', 'إرهاب', 'عملية عسكرية'
        ]

        # --- LOGIC ENGINE ---
        
        is_ksa = any(k in text_lower for k in ksa_keywords)
        is_threat = any(k in text_lower for k in threat_keywords)
        is_forces = any(k in text_lower for k in military_forces_keywords)
        
        # Rule 1: Very Sensitive (حساس للغاية) - KSA Negative / Forces Negative
        if (is_ksa and is_threat) or (is_forces and is_threat):
            report.classification = IntelligenceReport.Classification.TOP_SECRET
            report.topic = 'THREAT_KSA'
            # report.severity = 'CRITICAL' # Use classification for now
            report.credibility_score = 100 # Flag for immediate attention
            
        # Rule 2: Sensitive (حساس) - KSA Internal/Reputation
        elif is_ksa and any(k in text_lower for k in internal_keywords):
            report.classification = IntelligenceReport.Classification.SECRET
            report.topic = 'INTERNAL_KSA'
            report.credibility_score = 90
            
        # Rule 3: Secret (سري) - KSA Achievements/Vision
        elif is_ksa and any(k in text_lower for k in vision_keywords):
            report.classification = IntelligenceReport.Classification.SECRET
            report.topic = 'VISION_2030'
            report.credibility_score = 85
            
        # Rule 4: Urgent (عاجل) - Regional Security
        elif any(k in text_lower for k in neighbors) and any(k in text_lower for k in critical_events):
            report.classification = IntelligenceReport.Classification.CONFIDENTIAL
            report.topic = 'REGIONAL_SECURITY'
            report.credibility_score = 95
            
        # Rule 5: Critical (حرج) - General Military Events
        elif any(k in text_lower for k in critical_events):
            report.classification = IntelligenceReport.Classification.TOP_SECRET
            report.topic = 'MILITARY_OPS'
            report.credibility_score = 80
            
        # Default
        else:
            report.classification = IntelligenceReport.Classification.UNCLASSIFIED
            report.topic = 'GENERAL_INTEL'
            
        report.save()
