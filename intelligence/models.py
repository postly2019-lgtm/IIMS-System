from django.db import models
from django.utils.translation import gettext_lazy as _

from django.conf import settings

class Source(models.Model):
    class SourceType(models.TextChoices):
        RSS = 'RSS', _('RSS Feed')
        API = 'API', _('API Endpoint')
        SOCIAL = 'SOC', _('Social Media')
        WEBSITE = 'WEB', _('موقع إخباري')
        MANUAL = 'MAN', _('إدخال يدوي')
        OTHER = 'OTH', _('أخرى')

    name = models.CharField(_("اسم المصدر"), max_length=255)
    url = models.URLField(_("رابط المصدر"), blank=True, null=True)
    source_type = models.CharField(_("نوع المصدر"), max_length=10, choices=SourceType.choices, default=SourceType.RSS)
    category = models.CharField(_("التصنيف/الدولة"), max_length=100, blank=True, help_text=_("مثال: صحف أمريكية، وكالات عالمية"))
    reliability_score = models.IntegerField(_("درجة الموثوقية"), default=50, help_text=_("من 0 إلى 100"))
    is_active = models.BooleanField(_("نشط"), default=True)
    last_fetched_at = models.DateTimeField(_("آخر تحديث"), null=True, blank=True)

    class Meta:
        verbose_name = _("مصدر")
        verbose_name_plural = _("المصادر")

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"


class IntelligenceReport(models.Model):
    class Classification(models.TextChoices):
        UNCLASSIFIED = 'U', _('غير مصنف')
        RESTRICTED = 'R', _('مقيد')
        CONFIDENTIAL = 'C', _('سري')
        SECRET = 'S', _('سري للغاية')
        TOP_SECRET = 'TS', _('للغاية سري')

    title = models.CharField(_("العنوان"), max_length=500)
    content = models.TextField(_("المحتوى"))
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name=_("المصدر"), related_name='reports')
    original_url = models.URLField(_("الرابط الأصلي"), max_length=500, blank=True, null=True)
    published_at = models.DateTimeField(_("تاريخ النشر"), null=True, blank=True)
    created_at = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)
    
    classification = models.CharField(_("التصنيف الأمني"), max_length=2, choices=Classification.choices, default=Classification.UNCLASSIFIED)
    
    # Analysis Fields
    credibility_score = models.IntegerField(_("درجة المصداقية"), default=0)
    sentiment_score = models.FloatField(_("تحليل المشاعر"), default=0.0) # -1.0 to 1.0
    severity = models.CharField(_("درجة الخطورة"), max_length=10, choices=[
        ('LOW', 'منخفض'),
        ('MEDIUM', 'متوسط'),
        ('HIGH', 'عالي'),
        ('CRITICAL', 'حرج/طارئ')
    ], default='LOW')
    
    class Topic(models.TextChoices):
        MILITARY = 'MILITARY', _('عسكري وحربي')
        SECURITY = 'SECURITY', _('أمني')
        ARMAMENT = 'ARMAMENT', _('تسليح')
        INTEL = 'INTEL', _('استخباراتي')
        MIL_TECH = 'MIL_TECH', _('تكنولوجيا عسكرية')
        MEDICAL = 'MEDICAL', _('طبي/أوبئة')
        OTHER = 'OTHER', _('عام/أخرى')

    topic = models.CharField(_("التصنيف الموضوعي"), max_length=20, choices=Topic.choices, default=Topic.OTHER)

    related_reports = models.ManyToManyField('self', blank=True, verbose_name=_("تقارير ذات صلة"))

    # Translation Fields
    original_language = models.CharField(_("اللغة الأصلية"), max_length=10, default='en')
    translated_title = models.CharField(_("العنوان المترجم"), max_length=500, blank=True, null=True)
    translated_content = models.TextField(_("المحتوى المترجم"), blank=True, null=True)
    # Sovereign Arabic Fields (Mission D)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=500, blank=True, null=True)
    content_ar = models.TextField(_("المحتوى (عربي)"), blank=True, null=True)
    
    processing_status = models.CharField(_("حالة المعالجة"), max_length=20, choices=[
        ('PENDING', 'قيد المعالجة'),
        ('COMPLETED', 'تمت المعالجة'),
        ('FAILED', 'فشل المعالجة')
    ], default='PENDING')

    # User Interaction
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_reports', blank=True, verbose_name=_("المفضلة"))

    class Meta:
        verbose_name = _("تقرير استخباراتي")
        verbose_name_plural = _("تقارير الاستخبارات")
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

class Entity(models.Model):
    class EntityType(models.TextChoices):
        PERSON = 'PER', _('شخص')
        ORGANIZATION = 'ORG', _('منظمة')
        LOCATION = 'LOC', _('موقع')
        EVENT = 'EVT', _('حدث')

    name = models.CharField(_("الاسم"), max_length=255)
    entity_type = models.CharField(_("النوع"), max_length=3, choices=EntityType.choices)
    reports = models.ManyToManyField(IntelligenceReport, related_name='entities', verbose_name=_("التقارير المرتبطة"))

    class Meta:
        verbose_name = _("كيان")
        verbose_name_plural = _("الكيانات")

    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()})"

class CriticalAlertRule(models.Model):
    class Severity(models.TextChoices):
        HIGH = 'HIGH', _('عالي')
        CRITICAL = 'CRITICAL', _('حرج/طارئ')

    name = models.CharField(_("اسم التنبيه"), max_length=200, help_text=_("مثال: الأزمة اليمنية، تسليح الحوثي"))
    keywords = models.TextField(_("الكلمات المفتاحية"), help_text=_("افصل بين الكلمات بفاصلة. مثال: يمن, حوثي, صاروخ"))
    region = models.CharField(_("المنطقة/الدولة"), max_length=100, blank=True)
    severity_level = models.CharField(_("مستوى الخطورة المطلوب"), max_length=10, choices=Severity.choices, default=Severity.CRITICAL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("المستخدم"))
    is_active = models.BooleanField(_("مفعل"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("قاعدة تنبيه حرج")
        verbose_name_plural = _("قواعد التنبيهات الحرجة")

    def __str__(self):
        return self.name

class IntelligenceNotification(models.Model):
    """
    Alerts for critical intelligence updates.
    """
    class Level(models.TextChoices):
        INFO = 'INFO', _('معلومة')
        WARNING = 'WARNING', _('تحذير')
        CRITICAL = 'CRITICAL', _('خطر/حرج')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(_("العنوان"), max_length=255)
    message = models.TextField(_("الرسالة"))
    level = models.CharField(_("المستوى"), max_length=10, choices=Level.choices, default=Level.INFO)
    is_read = models.BooleanField(_("تمت القراءة"), default=False)
    report = models.ForeignKey(IntelligenceReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    alert_rule = models.ForeignKey(CriticalAlertRule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("قاعدة التنبيه"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.level} - {self.title}"

class SovereignTerm(models.Model):
    class TermCategory(models.TextChoices):
        MILITARY = 'MILITARY', _('عسكري')
        POLITICAL = 'POLITICAL', _('سياسي')
        GENERAL = 'GENERAL', _('عام')

    english_term = models.CharField(_("المصطلح الإنجليزي"), max_length=100, unique=True)
    arabic_translation = models.CharField(_("الترجمة العربية السيادية"), max_length=100)
    is_regex = models.BooleanField(_("تعبير نمطي (Regex)"), default=False)
    category = models.CharField(_("التصنيف"), max_length=50, choices=TermCategory.choices, default=TermCategory.GENERAL)

    class Meta:
        verbose_name = _("مصطلح سيادي")
        verbose_name_plural = _("قاموس المصطلحات السيادية")

    def __str__(self):
        return f"{self.english_term} -> {self.arabic_translation}"

class IgnoredSource(models.Model):
    keyword = models.CharField(_("الكلمة المحظورة"), max_length=100, unique=True, help_text=_("جزء من الرابط أو اسم المصدر (مثال: sports, health)"))
    reason = models.CharField(_("سبب الحظر"), max_length=255, blank=True)
    is_active = models.BooleanField(_("نشط"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("نطاق/مصدر محظور")
        verbose_name_plural = _("قائمة حظر المصادر")

    def __str__(self):
        return self.keyword


class SearchConstraint(models.Model):
    class ConstraintType(models.TextChoices):
        KEYWORD = 'KEYWORD', _('كلمة')
        PHRASE = 'PHRASE', _('جملة')
        TITLE = 'TITLE', _('عنوان')

    term = models.CharField(_("نص القيد"), max_length=255, unique=True)
    constraint_type = models.CharField(_("نوع القيد"), max_length=20, choices=ConstraintType.choices, default=ConstraintType.KEYWORD)
    is_active = models.BooleanField(_("مفعل"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("قيد بحث استدلالي")
        verbose_name_plural = _("قيود البحث الاستدلالية")
        ordering = ['-created_at']

    def __str__(self):
        return self.term

class ClassificationRule(models.Model):
    name = models.CharField(_("اسم القاعدة"), max_length=100)
    keywords = models.TextField(_("الكلمات المفتاحية (OR)"), help_text=_("مفصولة بفاصلة. وجود أي منها يفعل القاعدة جزئياً."))
    required_keywords = models.TextField(_("كلمات الشرط (AND)"), blank=True, help_text=_("مفصولة بفاصلة. يجب توفر إحداها على الأقل لتفعيل القاعدة."))
    classification = models.CharField(_("التصنيف الناتج"), max_length=2, choices=IntelligenceReport.Classification.choices)
    severity = models.CharField(_("درجة الخطورة الناتجة"), max_length=10, choices=[
        ('LOW', 'منخفض'),
        ('MEDIUM', 'متوسط'),
        ('HIGH', 'عالي'),
        ('CRITICAL', 'حرج/طارئ')
    ], default='MEDIUM')
    topic = models.CharField(_("الموضوع الناتج"), max_length=50, default='GENERAL_INTEL')
    weight = models.IntegerField(_("الأولوية"), default=10, help_text=_("القواعد ذات الوزن الأعلى تطبق أولاً"))
    is_active = models.BooleanField(_("مفعل"), default=True)

    class Meta:
        verbose_name = _("قاعدة تصنيف سيادي")
        verbose_name_plural = _("قواعد التصنيف الآلي")
        ordering = ['-weight']

    def __str__(self):
        return f"{self.name} ({self.weight})"

class EntityExtractionPattern(models.Model):
    pattern = models.CharField(_("النمط/الكلمة"), max_length=100, unique=True)
    entity_type = models.CharField(_("نوع الكيان"), max_length=3, choices=Entity.EntityType.choices)
    
    class Meta:
        verbose_name = _("نمط استخراج كيان")
        verbose_name_plural = _("أنماط استخراج الكيانات")

    def __str__(self):
        return f"{self.pattern} -> {self.get_entity_type_display()}"
