from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class AgentInstruction(models.Model):
    """
    Stores the system prompts and configuration for the AI Agent.
    """
    name = models.CharField(_("اسم الإعداد"), max_length=100, default="Standard Protocol")
    system_prompt = models.TextField(
        _("التعليمات العليا (System Prompt)"), 
        help_text=_("التعليمات الأساسية التي تحكم سلوك الوكيل. مثال: أنت محلل استخباراتي خبير..."),
        default="""أنت "المحلل الذكي" (Intelligence Agent)، مستشار استراتيجي وخبير في الأمن القومي والاستخبارات.
مهمتك الأساسية: تزويد صانع القرار بتحليلات عميقة، دقيقة، وموثوقة.

التعليمات العليا (Core Directives):
1. **البحث العميق (Deep Search):** عند السؤال عن خبر أو حدث، لا تكتفِ بالسطحيات. ابحث في عمق المصادر المتاحة (المستندات المرفقة، التقارير السابقة) واستخرج المعلومات ذات الدلالة الأمنية.
2. **التحليل الاستخباراتي (Intelligence Analysis):**
   - استخدم منهجية "التقدير الاستخباراتي" (Intelligence Estimate).
   - حلل "ماذا يعني هذا؟" (Implications) وليس فقط "ماذا حدث؟".
   - حدد الأطراف الفاعلة (Actors)، الدوافع (Motives)، والقدرات (Capabilities).
3. **التقييم الأمني:** ركز على التهديدات المحتملة (المباشرة وغير المباشرة) وتأثيرها على الأمن القومي.
4. **الموضوعية والحياد:** قدم الحقائق مجردة، ثم اتبعها بتحليلك المهني. اذكر مستوى الثقة في المعلومات (عالي، متوسط، منخفض).
5. **الصياغة:** استخدم لغة عسكرية/استخباراتية رصينة وموجزة.

عندما يُطلب منك تحليل رابط أو نص:
- استخرج الكيانات الرئيسية (أشخاص، منظمات، مواقع).
- اربط المعلومات بالسياق العام للأحداث.
- قدم توصيات أمنية واضحة في الختام."""
    )
    is_active = models.BooleanField(_("نشط"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AgentDocument(models.Model):
    """
    Knowledge base documents uploaded by users for RAG.
    """
    title = models.CharField(_("عنوان المستند"), max_length=255)
    file = models.FileField(_("الملف"), upload_to='agent_docs/')
    content_text = models.TextField(_("المحتوى النصي"), blank=True, help_text=_("المحتوى المستخرج من الملف للبحث"))
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(_("تمت المعالجة"), default=False)

    def __str__(self):
        return self.title

class AgentSession(models.Model):
    """
    A chat session between a user and the agent.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_sessions')
    title = models.CharField(_("عنوان المحادثة"), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_interaction = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

class AgentMessage(models.Model):
    """
    Individual messages in a session.
    """
    class Role(models.TextChoices):
        USER = 'user', _('المستخدم')
        ASSISTANT = 'assistant', _('الوكيل الذكي')
        SYSTEM = 'system', _('النظام')

    session = models.ForeignKey(AgentSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.TextField(_("المحتوى"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metadata for citations or reasoning
    citations = models.JSONField(_("المراجع/المصادر"), blank=True, null=True)

    class Meta:
        ordering = ['created_at']
