from django.core.management.base import BaseCommand
from intelligence.models import ClassificationRule, EntityExtractionPattern, Entity, IntelligenceReport

class Command(BaseCommand):
    help = 'Seeds initial Classification Rules and Entity Patterns'

    def handle(self, *args, **options):
        self.seed_entity_patterns()
        self.seed_classification_rules()
        self.stdout.write(self.style.SUCCESS('Successfully seeded Analysis Rules'))

    def seed_entity_patterns(self):
        patterns = {
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
        
        count = 0
        for pat, etype in patterns.items():
            _, created = EntityExtractionPattern.objects.get_or_create(
                pattern=pat,
                defaults={'entity_type': etype}
            )
            if created: count += 1
        self.stdout.write(f"Seeded {count} entity patterns.")

    def seed_classification_rules(self):
        # Common lists
        ksa_keywords = 'saudi, ksa, riyadh, kingdom, bin salman, السعودية, المملكة, الرياض, سلمان, ولي العهد'
        forces_keywords = 'armed forces, royal guard, air force, navy, القوات المسلحة, الحرس الملكي, الجيش, القوات الجوية'
        threat_keywords = 'attack, violation, criticism, failure, human rights, khashoggi, yemen war, هجوم, انتهاك, انتقاد, فشل, حقوق انسان, حرب اليمن, تدخل, sanctions, عقوبات'
        internal_keywords = 'economy, oil, aramco, inflation, unemployment, debt, اقتصاد, نفط, أرامكو, تضخم, بطالة, ديون'
        vision_keywords = 'vision 2030, neom, project, launch, achievement, growth, رؤية 2030, نيوم, مشروع, إطلاق, إنجاز, نمو, تطور'
        neighbors = 'yemen, iran, iraq, jordan, kuwait, bahrain, qatar, uae, oman, houthi, اليمن, إيران, العراق, الأردن, الكويت, البحرين, قطر, الإمارات, عمان, حوثي'
        critical_events = 'war, explosion, bomb, killing, killed, withdrawal, disarmament, weapon, missile, drone, terror, حرب, انفجار, قنبلة, مقتل, قتل, انسحاب, نزع سلاح, سلاح, صاروخ, طائرة مسيرة, إرهاب, عملية عسكرية'

        rules = [
            {
                'name': 'KSA Threat / Critical',
                'keywords': threat_keywords,
                'required_keywords': ksa_keywords + ", " + forces_keywords,
                'classification': IntelligenceReport.Classification.TOP_SECRET,
                'severity': 'CRITICAL',
                'topic': 'THREAT_KSA',
                'weight': 100
            },
            {
                'name': 'KSA Internal / Reputation',
                'keywords': internal_keywords,
                'required_keywords': ksa_keywords,
                'classification': IntelligenceReport.Classification.SECRET,
                'severity': 'MEDIUM',
                'topic': 'INTERNAL_KSA',
                'weight': 80
            },
            {
                'name': 'KSA Vision 2030',
                'keywords': vision_keywords,
                'required_keywords': ksa_keywords,
                'classification': IntelligenceReport.Classification.SECRET,
                'severity': 'LOW',
                'topic': 'VISION_2030',
                'weight': 70
            },
            {
                'name': 'Regional Security Crisis',
                'keywords': critical_events,
                'required_keywords': neighbors,
                'classification': IntelligenceReport.Classification.CONFIDENTIAL,
                'severity': 'HIGH',
                'topic': 'REGIONAL_SECURITY',
                'weight': 90
            },
            {
                'name': 'General Military Operations',
                'keywords': critical_events,
                'required_keywords': '',
                'classification': IntelligenceReport.Classification.TOP_SECRET,
                'severity': 'HIGH',
                'topic': 'MILITARY_OPS',
                'weight': 60
            }
        ]

        count = 0
        for rule in rules:
            _, created = ClassificationRule.objects.get_or_create(
                name=rule['name'],
                defaults={
                    'keywords': rule['keywords'],
                    'required_keywords': rule['required_keywords'],
                    'classification': rule['classification'],
                    'severity': rule['severity'],
                    'topic': rule['topic'],
                    'weight': rule['weight']
                }
            )
            if created: count += 1
        self.stdout.write(f"Seeded {count} classification rules.")
