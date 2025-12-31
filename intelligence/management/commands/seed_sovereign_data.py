from django.core.management.base import BaseCommand
from intelligence.models import SovereignTerm, IgnoredSource
import re

class Command(BaseCommand):
    help = 'Seeds initial Sovereign Terms and Ignored Sources from legacy code'

    def handle(self, *args, **options):
        self.seed_ignored_sources()
        self.seed_sovereign_terms()
        self.stdout.write(self.style.SUCCESS('Successfully seeded Sovereign Data'))

    def seed_ignored_sources(self):
        ignored_keywords = [
            'nature.com', 'medical', 'health', 'clinic', 'science daily', 
            'techcrunch', 'gadget', 'sports', 'entertainment', 'celebrity',
            'nature journal', 'phys.org', 'new scientist'
        ]
        
        count = 0
        for keyword in ignored_keywords:
            obj, created = IgnoredSource.objects.get_or_create(
                keyword=keyword,
                defaults={'reason': 'Initial System Seed'}
            )
            if created:
                count += 1
        self.stdout.write(f"Seeded {count} ignored sources.")

    def seed_sovereign_terms(self):
        # 1. Military Terminology
        military_terms = {
            r'\bwar\b': 'حرب',
            r'\bbattle\b': 'معركة',
            r'\battack\b': 'هجوم',
            r'\bstrike\b': 'ضربة',
            r'\bmissile\b': 'صاروخ',
            r'\bdrone\b': 'طائرة مسيرة',
            r'\buav\b': 'طائرة بدون طيار',
            r'\barmy\b': 'الجيش',
            r'\bnavy\b': 'البحرية',
            r'\bair force\b': 'القوات الجوية',
            r'\btroops\b': 'قوات',
            r'\bsoldiers\b': 'جنود',
            r'\bcasualty\b': 'إصابة',
            r'\bkilled\b': 'مقتل',
            r'\bdead\b': 'قتلى',
            r'\bweapon\b': 'سلاح',
            r'\bnuclear\b': 'نووي',
            r'\batomic\b': 'ذري',
            r'\bballistic\b': 'باليستي',
            r'\bdefense\b': 'دفاع',
            r'\bsecurity\b': 'أمن',
            r'\bintelligence\b': 'استخبارات',
            r'\bspy\b': 'جاسوس',
            r'\bterrorism\b': 'إرهاب',
            r'\bterrorist\b': 'إرهابي',
            r'\bmilitia\b': 'ميليشيا',
            r'\binsurgents\b': 'متمردين',
            r'\bbase\b': 'قاعدة',
            r'\boperation\b': 'عملية',
            r'\btarget\b': 'هدف',
            r'\bdestroy\b': 'تدمير',
            r'\blaunch\b': 'إطلاق',
            r'\bdeployed\b': 'نشر',
            r'\bwithdraw\b': 'انسحاب',
            r'\bpeacekeeping\b': 'حفظ السلام',
            r'\balliance\b': 'تحالف',
            r'\bcoalition\b': 'تحالف',
        }

        # 2. Political Terminology
        political_terms = {
            r'\bpresident\b': 'الرئيس',
            r'\bprime minister\b': 'رئيس الوزراء',
            r'\bminister\b': 'وزير',
            r'\bking\b': 'الملك',
            r'\bprince\b': 'الأمير',
            r'\bcrown prince\b': 'ولي العهد',
            r'\bgovernment\b': 'حكومة',
            r'\bparliament\b': 'برلمان',
            r'\belection\b': 'انتخابات',
            r'\bvote\b': 'تصويت',
            r'\btreaty\b': 'معاهدة',
            r'\bagreement\b': 'اتفاقية',
            r'\bsummit\b': 'قمة',
            r'\bconference\b': 'مؤتمر',
            r'\bdiplomat\b': 'دبلوماسي',
            r'\bambassador\b': 'سفير',
            r'\bforeign ministry\b': 'وزارة الخارجية',
            r'\bpolicy\b': 'سياسة',
            r'\brelations\b': 'علاقات',
            r'\bsanctions\b': 'عقوبات',
            r'\bunited nations\b': 'الأمم المتحدة',
            r'\bsecurity council\b': 'مجلس الأمن',
            r'\beu\b': 'الاتحاد الأوروبي',
            r'\bnato\b': 'الناتو',
        }

        # 3. Geopolitics & Countries (General)
        geo_terms = {
            r'\bsaudi arabia\b': 'المملكة العربية السعودية',
            r'\bksa\b': 'السعودية',
            r'\briyadh\b': 'الرياض',
            r'\byemen\b': 'اليمن',
            r'\bsanaa\b': 'صنعاء',
            r'\bhouthi\b': 'الحوثي',
            r'\biran\b': 'إيران',
            r'\btehran\b': 'طهران',
            r'\biraq\b': 'العراق',
            r'\bbaghdad\b': 'بغداد',
            r'\bsyria\b': 'سوريا',
            r'\bdamascus\b': 'دمشق',
            r'\blebanon\b': 'لبنان',
            r'\bbeirut\b': 'بيروت',
            r'\bjordan\b': 'الأردن',
            r'\bamman\b': 'عمان',
            r'\begypt\b': 'مصر',
            r'\bcairo\b': 'القاهرة',
            r'\buae\b': 'الإمارات',
            r'\babudhabi\b': 'أبوظبي',
            r'\bdubai\b': 'دبي',
            r'\bqatar\b': 'قطر',
            r'\bdoha\b': 'الدوحة',
            r'\bkuwait\b': 'الكويت',
            r'\bbahrain\b': 'البحرين',
            r'\bmanama\b': 'المنامة',
            r'\boman\b': 'عمان',
            r'\bmuscat\b': 'مسقط',
            r'\bisrael\b': 'إسرائيل',
            r'\btel aviv\b': 'تل أبيب',
            r'\bjerusalem\b': 'القدس',
            r'\bgaza\b': 'غزة',
            r'\bwest bank\b': 'الضفة الغربية',
            r'\busa\b': 'الولايات المتحدة',
            r'\bus\b': 'أمريكا',
            r'\bwashington\b': 'واشنطن',
            r'\buk\b': 'بريطانيا',
            r'\blondon\b': 'لندن',
            r'\bfrance\b': 'فرنسا',
            r'\bparis\b': 'باريس',
            r'\bgermany\b': 'ألمانيا',
            r'\bberlin\b': 'برلين',
            r'\brussia\b': 'روسيا',
            r'\bmoscow\b': 'موسكو',
            r'\bchina\b': 'الصين',
            r'\bbeijing\b': 'بكين',
        }
        
        count = 0
        
        for term, trans in military_terms.items():
            _, created = SovereignTerm.objects.get_or_create(
                english_term=term,
                defaults={'arabic_translation': trans, 'category': 'MILITARY', 'is_regex': True}
            )
            if created: count += 1

        for term, trans in political_terms.items():
            _, created = SovereignTerm.objects.get_or_create(
                english_term=term,
                defaults={'arabic_translation': trans, 'category': 'POLITICAL', 'is_regex': True}
            )
            if created: count += 1
            
        for term, trans in geo_terms.items():
            _, created = SovereignTerm.objects.get_or_create(
                english_term=term,
                defaults={'arabic_translation': trans, 'category': 'GENERAL', 'is_regex': True}
            )
            if created: count += 1

        self.stdout.write(f"Seeded {count} sovereign terms.")
