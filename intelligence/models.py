from django.db import models
from django.utils.translation import gettext_lazy as _

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
    related_reports = models.ManyToManyField('self', blank=True, verbose_name=_("تقارير ذات صلة"))

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
