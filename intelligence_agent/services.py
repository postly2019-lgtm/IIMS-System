import os
import logging
from django.conf import settings
from .models import AgentInstruction, AgentMessage

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
        instruction = AgentInstruction.objects.filter(is_active=True).first()
        if instruction:
            return instruction.system_prompt
        return "You are a helpful AI assistant."

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
        messages.append({"role": "system", "content": system_prompt})

        # Chat History (Last 10 messages for context window management)
        # In a real RAG system, we would select relevant history based on vector similarity
        history = session.messages.all().order_by('created_at')[:10] 
        for msg in history:
            role = "user" if msg.role == AgentMessage.Role.USER else "assistant"
            messages.append({"role": role, "content": msg.content})

        # Current Message (Already added to DB by view? If not, add it here)
        # Assuming the view adds the user message to DB before calling this service
        # If the view passes the content string but hasn't saved it yet, we add it to the list
        # But usually we want to include the current message.
        # Let's assume the view handles saving the user message to DB first.
        # So it's already in `history` if we query all.
        # However, `history` above queries all messages.
        # If `user_message_content` is passed separately, we might want to ensure we don't duplicate.
        # Let's verify how we'll call this.
        
        # Refined approach: 
        # The view creates the User Message object.
        # Then calls this service.
        # So `session.messages.all()` includes the latest user message.
        
        # 2. Call API
        try:
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                temperature=0.7,
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
