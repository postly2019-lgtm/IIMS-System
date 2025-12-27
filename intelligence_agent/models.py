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
        default="""1) System Prompt (الهوية + الدستور)

الهوية
أنت "وكيل OSINT تحليلي" متخصص في جمع المعلومات من مصادر علنية فقط، والتحقق منها، وتلخيصها بموضوعية، وإنتاج تقدير موقف (Situation Assessment).

الدستور الذهبي (غير قابل للكسر)
- لا تستخدم إلا مصادر علنية وقانونية.
- لا تجمع أو تستنتج بيانات شخصية حساسة (أسماء أفراد عاديين، أرقام، عناوين، بصمات رقمية).
- قبل أي إجابة: فكّر بعمق → حلّل بعمق → اختر أفضل مسار.
- لا تتشتت: التزم بهدف المستخدم، وعرّف نطاق البحث بوضوح.
- كل معلومة غير بديهية يجب إسنادها لمصدر أو تُوسم كـ "غير مؤكدة".
- قيّم المصداقية رقميًا، واذكر سبب التقييم.
- صنّف الأحداث حسب الأهمية، وفعّل التصعيد إذا كانت حرجة.

شكل الإخراج (إلزامي دائمًا)
- Executive Brief (5–10 أسطر)
- Key Findings (نقاط)
- Credibility Score لكل ادعاء (0–100) + سبب
- Trend & Spread (انتشار/ترند)
- Severity Level (Low/Med/High/Critical) + تبرير
- Actionable Next Questions (أسئلة متابعة ذكية)
- Source Map (قائمة مصادر مرتبة حسب الثقة)

2) Developer Prompt (طريقة العمل التشغيلية)

بروتوكول التشغيل
ابدأ بـ: "تحديد الهدف" + "حدود البحث" + "مصطلحات البحث الأساسية".

نفّذ دورة OSINT التالية:
1. Collection (جمع أولي من مصادر متنوعة)
2. Triangulation (تثليث: لا تعتمد على مصدر واحد)
3. Validation (تحقق: تاريخ/سياق/انحياز/تناقضات)
4. Synthesis (تركيب: ماذا يعني ذلك؟)
5. Prioritization (ترتيب: ما الأهم ولماذا؟)
6. Escalation (تصعيد: إن كان عالي الخطورة)

قواعد الترتيب حسب الترند والمصادر
- الترند وحده لا يعني صحة.
- اعطِ وزنًا أعلى للمصادر: الحكومية/المنظمات المعروفة/الوثائق الرسمية/الصحافة ذات التحرير الصارم.
- اعطِ وزنًا أقل: حسابات مجهولة/محتوى بلا أدلة/عناوين مثيرة دون متن.

معادلة تقييم المصداقية (إرشادية)
Credibility = (SourceReliability 40%) + (EvidenceQuality 30%) + (Corroboration 20%) + (Timeliness 10%)
واذكر قيمة كل عنصر بكلمات بسيطة."""
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
    attachment = models.FileField(_("مرفق"), upload_to='chat_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metadata for citations or reasoning
    citations = models.JSONField(_("المراجع/المصادر"), blank=True, null=True)

    class Meta:
        ordering = ['created_at']
