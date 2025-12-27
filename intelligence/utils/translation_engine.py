import re

class SmartDictionaryTranslator:
    """
    A sovereign, offline translation engine optimized for military and political intelligence.
    Does not rely on external APIs or AI agents.
    Uses extensive pattern matching and terminology mapping.
    """

    def __init__(self):
        # 1. Military Terminology
        self.military_terms = {
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
        self.political_terms = {
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

        # 3. Geopolitics & Countries
        self.geo_terms = {
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
        
        # 4. Common Verbs/Connectors (To make sentences somewhat readable)
        self.common_terms = {
            r'\bsays\b': 'يقول',
            r'\bsaid\b': 'قال',
            r'\breports\b': 'تقارير',
            r'\bwarns\b': 'يحذر',
            r'\bannounces\b': 'يعلن',
            r'\bclaims\b': 'يزعم',
            r'\bdenies\b': 'ينفي',
            r'\bconfirms\b': 'يؤكد',
            r'\bin\b': 'في',
            r'\bon\b': 'على',
            r'\bto\b': 'إلى',
            r'\bfrom\b': 'من',
            r'\bwith\b': 'مع',
            r'\bagainst\b': 'ضد',
            r'\band\b': 'و',
            r'\bnew\b': 'جديد',
            r'\burgent\b': 'عاجل',
            r'\bbreaking\b': 'عاجل',
        }

    def translate_text(self, text):
        """
        Translates text using regex-based dictionary substitution.
        Preserves numbers and punctuation.
        """
        if not text:
            return ""

        # Lowercase for matching, but we might lose casing info (acceptable for Arabic)
        # Actually, let's keep original for reconstruction if needed, but match lower
        
        translated_text = text
        
        # Combine all dictionaries
        all_maps = {**self.military_terms, **self.political_terms, **self.geo_terms, **self.common_terms}
        
        # Sort by length (descending) to match longest phrases first (e.g., "Prime Minister" before "Minister")
        sorted_patterns = sorted(all_maps.keys(), key=len, reverse=True)
        
        for pattern in sorted_patterns:
            target = all_maps[pattern]
            # Case insensitive replacement
            translated_text = re.sub(pattern, target, translated_text, flags=re.IGNORECASE)
            
        return translated_text

# Singleton Instance
translator = SmartDictionaryTranslator()
