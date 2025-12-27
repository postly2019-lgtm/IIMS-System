import os
import logging
from django.conf import settings
from .models import AgentInstruction, AgentMessage
from intelligence.models import IntelligenceReport
from django.db.models import Q

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        try:
            from groq import Groq
            api_key = settings.GROQ_API_KEY
            if not api_key:
                logger.warning("GROQ_API_KEY is not set.")
                self.client = None
            else:
                self.client = Groq(api_key=api_key)
        except ImportError:
            logger.error("Groq SDK not installed.")
            self.client = None

    def get_system_prompt(self):
        """Retrieve the active system prompt."""
        # Use active instructions first
        instruction = AgentInstruction.objects.filter(is_active=True).first()
        if instruction:
            return instruction.system_prompt
            
        # Fallback default prompt (OSINT Standard) if database is empty
        return """1) System Prompt (الهوية + الدستور)

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

    def get_relevant_context(self, query):
        """
        Retrieves relevant intelligence reports from the database based on the query.
        Simple Keyword Search RAG.
        """
        if not query:
            return ""

        # Search in title, content, and entities
        reports = IntelligenceReport.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(entities__name__icontains=query)
        ).order_by('-published_at', '-credibility_score')[:10]

        if not reports.exists():
            return ""

        context_str = "\n--- تقارير استخباراتية ذات صلة (Internal Intelligence Reports) ---\n"
        for report in reports:
            context_str += f"- [ID:{report.id}] {report.published_at.strftime('%Y-%m-%d')}: {report.title}\n"
            context_str += f"  المصدر: {report.source.name} (Credibility: {report.credibility_score})\n"
            context_str += f"  المحتوى: {report.content[:300]}...\n\n"
        
        return context_str

    def translate_text(self, title, content):
        """
        Translates text to Arabic using the LLM.
        """
        if not self.client:
            return None

        prompt = f"""
        Translate the following Intelligence Report into professional Arabic.
        Maintain military and political terminology.
        
        Title: {title}
        Content: {content}
        
        Output Format:
        Title: [Arabic Title]
        Content: [Arabic Content]
        """

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2048,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Translation Error: {e}")
            return None

    def chat_completion(self, session, user_message_content):
        """
        Send message to Groq API and return the response.
        """
        if not self.client:
            return "⚠️ عذراً، خدمة الذكاء الاصطناعي غير متصلة.\nيرجى الذهاب إلى صفحة 'إعدادات الوكيل' (Agent Settings) وإضافة مفتاح GROQ_API_KEY."

        # 1. Prepare History
        messages = []
        
        # System Prompt
        system_prompt = self.get_system_prompt()
        
        # 2. Get RAG Context (from internal reports)
        # We use the current user message content to find relevant reports
        context_data = self.get_relevant_context(user_message_content)
        
        if context_data:
            system_prompt += f"\n\n{context_data}\n\nاستخدم التقارير أعلاه للإجابة بدقة ومصداقية. إذا لم تجد معلومات كافية، صرح بذلك."

        messages.append({"role": "system", "content": system_prompt})

        # Chat History (Last 10 messages)
        # Fix: Get RECENT messages (descending), then reverse to chronological
        recent_messages = list(session.messages.all().order_by('-created_at')[:10])
        recent_messages.reverse() # Now in chronological order (Oldest -> Newest)

        for msg in recent_messages:
            role = "user" if msg.role == AgentMessage.Role.USER else "assistant"
            content = msg.content
            
            # INJECT ENHANCED CONTEXT:
            # If this is the very last message (current user input), use the 'user_message_content' 
            # passed to this function, which contains file attachments/context not yet saved in DB content.
            if msg == recent_messages[-1] and role == "user":
                content = user_message_content
            
            messages.append({"role": role, "content": content})

        # 3. Call API
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.6, # Lower temperature for more factual/analytical responses
                max_tokens=2048,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            ai_response = completion.choices[0].message.content
            return ai_response

        except Exception as e:
            logger.error(f"Groq API Error: {str(e)}")
            return f"System Error: Unable to process request. {str(e)}"
