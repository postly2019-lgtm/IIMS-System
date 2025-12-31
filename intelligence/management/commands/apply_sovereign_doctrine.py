from django.core.management.base import BaseCommand
from intelligence.models import ClassificationRule, IntelligenceReport

class Command(BaseCommand):
    help = 'Applies Sovereign Classification Doctrine Rules'

    def handle(self, *args, **options):
        self.stdout.write("Applying Sovereign Classification Doctrine...")
        
        # Define the Sovereign Doctrine Rules
        # Structure: (Name, Keywords(OR), Required(AND), Class, Severity, Topic, Weight)
        doctrine_rules = [
            (
                "Threat to Leadership (تهديد القيادة)",
                "assassination,coup,overthrow,regime change,king,crown prince,royal family,اغتيال,انقلاب,إسقاط نظام,الملك,ولي العهد,الأسرة الحاكمة",
                "plot,plan,attack,target,threat,مؤامرة,خطة,هجوم,استهداف,تهديد",
                IntelligenceReport.Classification.TOP_SECRET,
                'CRITICAL',
                'THREAT_LEADERSHIP',
                100
            ),
            (
                "Ballistic/Drone Threat (تهديد صاروخي/مسيرات)",
                "missile,drone,uav,ballistic,houthi,intercepted,air defense,صاروخ,مسيرة,طائرة بدون طيار,باليستي,حوثي,اعتراض,دفاع جوي",
                "attack,fired,launched,strike,target,هجوم,إطلاق,ضربة,استهداف",
                IntelligenceReport.Classification.TOP_SECRET,
                'CRITICAL',
                'MILITARY_OPS',
                95
            ),
            (
                "Critical Infrastructure (البنية التحتية الحساسة)",
                "aramco,oil field,pipeline,refinery,desalination,power plant,airport,أرامكو,حقل نفط,أنبوب نفط,مصفاة,تحلية,محطة كهرباء,مطار",
                "attack,fire,explosion,cyber,hack,breach,sabotage,هجوم,حريق,انفجار,سيبراني,اختراق,تخريب",
                IntelligenceReport.Classification.SECRET,
                'HIGH',
                'INFRASTRUCTURE',
                90
            ),
            (
                "Border Security (أمن الحدود)",
                "border,infiltration,smuggling,clash,guard,حدود,تسلل,تهريب,اشتباك,حرس الحدود",
                "killed,injured,arrest,weapon,drug,explosive,مقتل,إصابة,اعتقال,سلاح,مخدرات,متفجرات",
                IntelligenceReport.Classification.CONFIDENTIAL,
                'HIGH',
                'BORDER_SECURITY',
                85
            ),
             (
                "Vision 2030 Strategic (استراتيجية الرؤية)",
                "vision 2030,neom,the line,red sea project,qiddiya,roshn,pif,public investment fund,رؤية 2030,نيوم,ذا لاين,البحر الأحمر,القدية,روشن,صندوق الاستثمارات",
                "launch,invest,partnership,agreement,ipo,إطلاق,استثمار,شراكة,اتفاقية,اكتتاب",
                IntelligenceReport.Classification.CONFIDENTIAL,
                'LOW',
                'VISION_2030',
                70
            ),
            (
                "Regional Instability (عدم استقرار إقليمي)",
                "yemen,iran,iraq,lebanon,syria,sudan,اليمن,إيران,العراق,لبنان,سوريا,السودان",
                "protest,riot,war,conflict,militia,crisis,احتجاج,شغب,حرب,نزاع,ميليشيا,أزمة",
                IntelligenceReport.Classification.RESTRICTED,
                'MEDIUM',
                'REGIONAL_POLITICS',
                60
            ),
            (
                "Anti-State Propaganda (دعاية معادية)",
                "human rights,activist,detained,freedom of speech,boycott,حقوق إنسان,ناشط,معتقل,حرية تعبير,مقاطعة",
                "report,condemn,criticize,violation,تقرير,إدانة,انتقاد,انتهاك",
                IntelligenceReport.Classification.RESTRICTED,
                'LOW',
                'PROPAGANDA',
                50
            )
        ]

        created_count = 0
        updated_count = 0

        for rule_data in doctrine_rules:
            name, keywords, required, classification, severity, topic, weight = rule_data
            
            obj, created = ClassificationRule.objects.update_or_create(
                name=name,
                defaults={
                    'keywords': keywords,
                    'required_keywords': required,
                    'classification': classification,
                    'severity': severity,
                    'topic': topic,
                    'weight': weight,
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully Applied Doctrine: {created_count} Created, {updated_count} Updated."))
