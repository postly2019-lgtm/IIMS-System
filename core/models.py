from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import qrcode
from io import BytesIO
from django.core.files import File

class User(AbstractUser):
    class Rank(models.TextChoices):
        MILITARY = 'MIL', _('عسكري')
        CIVILIAN = 'CIV', _('مدني')

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('مدير النظام (Admin)')
        MANAGER = 'MANAGER', _('مدير (System Manager)')
        ANALYST = 'ANALYST', _('محلل (Analyst)')

    job_number = models.CharField(_("الرقم الوظيفي"), max_length=20, unique=True, null=True, blank=False)
    mobile_number = models.CharField(_("رقم الجوال"), max_length=15, null=True, blank=True)
    rank = models.CharField(_("الرتبة"), max_length=10, choices=Rank.choices, default=Rank.CIVILIAN)
    role = models.CharField(_("الدور الوظيفي"), max_length=10, choices=Role.choices, default=Role.ANALYST)
    photo = models.ImageField(_("الصورة الشخصية"), upload_to='users/photos/', null=True, blank=True)
    qr_code = models.ImageField(_("رمز الاستجابة السريعة"), upload_to='users/qrcodes/', null=True, blank=True)
    
    # Security flag: if True, password login is disabled (conceptually)
    requires_smart_card = models.BooleanField(_("تطلب بطاقة ذكية"), default=True)

    class Meta:
        verbose_name = _("مستخدم")
        verbose_name_plural = _("المستخدمين")

    def save(self, *args, **kwargs):
        if self.rank not in (self.Rank.MILITARY, self.Rank.CIVILIAN):
            self.rank = self.Rank.MILITARY
        
        
        if not self.qr_code and self.username:
            qr_data = f"USER:{self.username}|JOB:{self.job_number}|UID:{self.id}"
            qr_image = qrcode.make(qr_data)
            canvas = BytesIO()
            qr_image.save(canvas, format='PNG')
            file_name = f'qr_{self.username}.png'
            self.qr_code.save(file_name, File(canvas), save=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class UserActionLog(models.Model):
    class ActionType(models.TextChoices):
        LOGIN = 'LOGIN', _('تسجيل دخول')
        LOGOUT = 'LOGOUT', _('تسجيل خروج')
        VIEW_REPORT = 'VIEW', _('عرض تقرير')
        SEARCH = 'SEARCH', _('بحث')
        PRINT_REPORT = 'PRINT', _('طباعة تقرير')
        EXPORT = 'EXPORT', _('تصدير بيانات')
        ACCESS_DENIED = 'DENIED', _('محاولة وصول مرفوضة')
        OTHER = 'OTHER', _('أخرى')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("المستخدم"), related_name='audit_logs')
    action = models.CharField(_("الإجراء"), max_length=10, choices=ActionType.choices)
    target_object = models.CharField(_("الهدف"), max_length=255, blank=True, help_text="Report ID, Search Query, etc.")
    details = models.TextField(_("التفاصيل"), blank=True)
    ip_address = models.GenericIPAddressField(_("عنوان IP"), null=True, blank=True)
    timestamp = models.DateTimeField(_("التوقيت"), auto_now_add=True)

    class Meta:
        verbose_name = _("سجل نشاط")
        verbose_name_plural = _("سجلات الأنشطة")
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
