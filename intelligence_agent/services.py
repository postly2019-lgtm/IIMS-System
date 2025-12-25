import os
import json
from django.conf import settings
from .models import AgentInstruction, AgentMessage

class AIService:
    """
    Service to handle interactions with the AI Model (e.g., Groq/Llama 3).
    """
    
    def __init__(self):
        # In a real scenario, we would use os.environ.get("GROQ_API_KEY")
        # For this implementation, we will simulate the response if no key is present.
        self.api_key = os.environ.get("GROQ_API_KEY")
        
    def get_system_prompt(self):
        """Retrieves the active system prompt."""
        instruction = AgentInstruction.objects.filter(is_active=True).first()
        if instruction:
            return instruction.system_prompt
        return "You are a helpful intelligence assistant."

    def generate_response(self, session, user_message_content):
        """
        Generates a response based on the conversation history and RAG.
        """
        # 1. Save User Message
        AgentMessage.objects.create(
            session=session,
            role=AgentMessage.Role.USER,
            content=user_message_content
        )

        # 2. Build Context (History + RAG)
        # TODO: Implement RAG (Search Documents & Intelligence Reports)
        # For now, we just take the last 10 messages
        history = AgentMessage.objects.filter(session=session).order_by('-created_at')[:10:-1]
        
        # 3. Call AI Model
        # Mocking the response for now as we don't have a real API Key in this env
        response_text = self._mock_inference(user_message_content)

        # 4. Save Assistant Message
        msg = AgentMessage.objects.create(
            session=session,
            role=AgentMessage.Role.ASSISTANT,
            content=response_text
        )
        return msg

    def _mock_inference(self, prompt):
        """
        Simulates an intelligent response for demonstration purposes.
        """
        prompt_lower = prompt.lower()
        if "تحليل" in prompt_lower or "analyze" in prompt_lower:
            return (
                "**تحليل استخباراتي أولي:**\n\n"
                "بناءً على المعطيات المقدمة، يمكن استخلاص النقاط التالية:\n"
                "1. **المؤشرات الأولية:** تشير المعلومات إلى تصاعد في النشاط.\n"
                "2. **التقييم:** مستوى التهديد يعتبر متوسطاً مع احتمالية للتصعيد.\n"
                "3. **التوصيات:** يوصى بمراقبة المصادر المفتوحة وتكثيف البحث في المناطق المذكورة.\n\n"
                "*هذا رد تلقائي (محاكاة) نظراً لعدم توفر مفتاح API فعلي.*"
            )
        elif "بحث" in prompt_lower or "search" in prompt_lower:
             return (
                "**نتائج البحث:**\n\n"
                "قمت بالبحث في المصادر المتاحة (التقارير الداخلية والمستندات).\n"
                "- لم يتم العثور على تطابق دقيق في قاعدة البيانات الحالية.\n"
                "- يرجى تزويدي بمزيد من التفاصيل أو كلمات مفتاحية محددة."
            )
        else:
            return (
                "أهلاً بك. أنا وكيلك الذكي للمهام الاستخباراتية.\n"
                "يمكنني مساعدتك في:\n"
                "- تحليل المقالات والروابط.\n"
                "- البحث في الأرشيف.\n"
                "- تقديم تقديرات موقف.\n\n"
                "كيف يمكنني خدمتك اليوم؟"
            )
