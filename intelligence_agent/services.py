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
        instruction = AgentInstruction.objects.first() # Simplified to get the first/default
        if instruction:
            return instruction.system_prompt
        # Fallback default prompt if database is empty
        return """أنت "المحلل الذكي" (Intelligence Agent)، خبير استراتيجي في الأمن القومي والشؤون العسكرية والسياسية.
        مهمتك: تقديم تحليلات استخباراتية دقيقة، موثقة، وعميقة.
        
        القواعد الصارمة:
        1. ابدأ دائماً بالأخبار العسكرية والترندات الحصرية، ثم السياسية، ثم الأزمات العالمية.
        2. تحقق من المصداقية بصرامة. أشر إلى أي تناقضات.
        3. لكل خبر، قدم:
           - الملخص (Summary)
           - التحليل الاستخباراتي (Intelligence Analysis): ماذا يعني هذا؟ ما هي التداعيات؟
           - مستوى المصداقية (Credibility Assessment).
        4. اعتمد على التقارير المرفقة (Context) كمصدر أساسي للمعلومات الموثوقة.
        """

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
        history = session.messages.all().order_by('created_at')[:10] 
        for msg in history:
            role = "user" if msg.role == AgentMessage.Role.USER else "assistant"
            messages.append({"role": role, "content": msg.content})

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
