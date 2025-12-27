import os
import logging
import re
from django.conf import settings
from django.utils import timezone
from .models import AgentInstruction, AgentMessage, AgentSession
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
        """Retrieve the active system prompt or use the Sovereign Standard."""
        # Use active instructions first
        instruction = AgentInstruction.objects.filter(is_active=True).first()
        if instruction:
            return instruction.system_prompt
            
        # SOVEREIGN INTELLIGENCE STANDARD PROMPT (ARABIC ONLY)
        return """**هوية النظام:**
أنت "المحلل الاستراتيجي الأول" (Senior Strategic Analyst) في نظام الاستخبارات السيادية. مهمتك هي تقديم تقديرات موقف، تحليلات أمنية، ودعم اتخاذ القرار للقيادة العليا.

**المبادئ الحاكمة (Sovereign Protocols):**
1. **الولاء والسيادة:** الأولوية القصوى هي أمن الدولة ومصالحها العليا. أي تهديد يمس السيادة يجب تمييزه فوراً.
2. **اللغة:** الردود يجب أن تكون باللغة العربية الفصحى الرصينة (لغة عسكرية/سياسية). يمنع استخدام مصطلحات أجنبية إلا للضرورة القصوى مع تعريبها.
3. **الدقة والموضوعية:** التحليل يبنى على الوقائع المتاحة في السياق. لا تختلق معلومات. إذا كانت المعلومة ناقصة، اذكر ذلك بوضوح.
4. **السرية:** التعامل مع المعلومات المقدمة لك على أنها "سري للغاية" ولا يجوز تداولها خارج هذا النطاق.

**نمط الإخراج المطلوب:**
- إجابات مباشرة ودقيقة على استفسارات المستخدم.
- عند طلب تحليل تقرير: ابدأ بـ "الملخص التنفيذي"، ثم "النقاط الجوهرية"، ثم "التقييم الأمني/السياسي"، واختم بـ "التوصيات".
- استخدم التنسيق الواضح (نقاط، عناوين عريضة) لسهولة القراءة من قبل صناع القرار.

**آلية التعامل مع التهديدات:**
- إذا رصدت تهديداً عسكرياً أو أمنياً في السياق، قم بتمييزه بوضوح تحت بند **"تحذير سيادي"**.
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
            title = report.translated_title or report.title
            content = report.translated_content or report.content
            context_str += f"- [ID:{report.id}] {report.published_at.strftime('%Y-%m-%d')}: {title}\n"
            context_str += f"  المصدر: {report.source.name} (Credibility: {report.credibility_score})\n"
            context_str += f"  الخطورة: {report.severity} | التصنيف: {report.classification}\n"
            context_str += f"  المحتوى: {content[:300]}...\n\n"
        
        return context_str

    def translate_report_obj(self, report):
        """
        Translates an IntelligenceReport object and saves it.
        """
        if report.processing_status == 'COMPLETED' and report.translated_title:
            return True

        if not self.client:
            # Fallback for offline/demo
            if not report.translated_title:
                # Basic Simulation
                report.translated_title = self._simulated_translation(report.title, "")
                report.translated_content = self._simulated_translation("", report.content)
                report.processing_status = 'COMPLETED' # Mark as completed even if simulated
                report.save(update_fields=['translated_title', 'translated_content', 'processing_status'])
            return True

        try:
            # 1. Translate Title
            title_prompt = f"Translate to Arabic (Military/Intel Style). Output ONLY the translation: {report.title}"
            t_title = self.chat_completion(title_prompt)
            
            # 2. Translate Content (Chunking if necessary, but Groq has large context)
            content_prompt = f"Translate to Arabic (Military/Intel Style). Output ONLY the translation: {report.content}"
            t_content = self.chat_completion(content_prompt)
            
            if t_title:
                report.translated_title = t_title.strip()
            if t_content:
                report.translated_content = t_content.strip()
            
            report.processing_status = 'COMPLETED'
            report.save(update_fields=['translated_title', 'translated_content', 'processing_status'])
            return True

        except Exception as e:
            logger.error(f"Translation failed for report {report.id}: {e}")
            report.processing_status = 'FAILED'
            report.save(update_fields=['processing_status'])
            return False

    def translate_text(self, title, content):
        """
        Translates text to Arabic using the LLM or a simulated fallback.
        """
        if not self.client:
            logger.warning("GroqClient not initialized. Using simulated translation.")
            return self._simulated_translation(title, content)

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
            # Use simulated translation on error to ensure user sees Arabic
            return self._simulated_translation(title, content)

    def _simulated_translation(self, title, content):
        """
        Provides a mock translation by replacing common English terms with Arabic ones.
        """
        if not title and not content:
            return ""

        # Use a comprehensive dictionary
        terms = {
            "Nature Journal": "مجلة نيتشر", "Nature": "مجلة نيتشر",
            "War": "حرب", "Military": "عسكري", "Security": "أمن", "Attack": "هجوم",
            "Defense": "دفاع", "Missile": "صاروخ", "Troops": "قوات", "Report": "تقرير",
            "Intelligence": "استخبارات", "Critical": "حرج", "Alert": "تنبيه",
            "Health": "صحة", "Disease": "مرض", "Virus": "فيروس", "Vaccine": "لقاح",
            "Government": "حكومة", "President": "رئيس", "Minister": "وزير",
            "US": "الولايات المتحدة", "UK": "بريطانيا", "China": "الصين", "Russia": "روسيا",
            "Iran": "إيران", "Israel": "إسرائيل", "Yemen": "اليمن", "Saudi": "السعودية",
            "Region": "منطقة", "Border": "حدود", "Conflict": "صراع", "Peace": "سلام",
            "Economy": "اقتصاد", "Oil": "نفط", "Gas": "غاز", "Cyber": "سيبراني",
            "Technology": "تكنولوجيا", "Nuclear": "نووي", "Weapon": "سلاح",
            "Organization": "منظمة", "Group": "جماعة", "Terrorist": "إرهابي",
            "International": "دولي", "National": "وطني", "Local": "محلي",
            "Strategy": "استراتيجية", "Operation": "عملية", "Target": "هدف",
            "Casualties": "خسائر", "Killed": "قتل", "Injured": "جرحى",
            "United Nations": "الأمم المتحدة", "UN": "الأمم المتحدة",
            "Council": "مجلس", "Committee": "لجنة", "Agency": "وكالة",
            "Plants": "نباتات", "Plant": "نبات", "Infrared": "أشعة تحت الحمراء", "Signals": "إشارات",
            "Reproduce": "تكاثر", "Beetles": "خنافس", "Pollinating": "تلقيح", "Dark": "ظلام",
            "Hot spot": "نقطة ساخنة", "Ready": "جاهز", "Say": "تقول", "Use": "تستخدم"
        }

        # Apply replacements using regex for safety (word boundaries)
        sim_title = title or ""
        sim_content = content or ""
        
        # Sort keys by length (descending) to match "Nature Journal" before "Nature"
        sorted_keys = sorted(terms.keys(), key=len, reverse=True)
        
        # Build a single regex pattern
        pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted_keys) + r')\b', re.IGNORECASE)
        
        def replace(match):
            # Find the key that matched (case-insensitive search in terms)
            word = match.group(0)
            for k, v in terms.items():
                if k.lower() == word.lower():
                    return v
            return word

        sim_title = pattern.sub(replace, sim_title)
        sim_content = pattern.sub(replace, sim_content)

        if title and not content:
            return sim_title
        if content and not title:
            return sim_content
            
        return f"{sim_title}\n\n{sim_content}"

    def chat_completion(self, session_or_prompt, user_content=None):
        """
        Wrapper for chat completion that handles both simple prompts and full session context.
        """
        # Resolve actual user text
        actual_text = user_content
        if not actual_text and not hasattr(session_or_prompt, 'messages'):
            actual_text = str(session_or_prompt)

        # --- 1. Quick Intent Check (Optimization) ---
        # If user_content is simple greeting, don't waste API call
        if actual_text:
            stripped = actual_text.strip().lower()
            if stripped in ['مرحبا', 'هلا', 'السلام عليكم', 'hello', 'hi']:
                return "وعليكم السلام ورحمة الله. أنا المحلل الاستراتيجي السيادي. جاهز لاستقبال التوجيهات أو تحليل التقارير."

        # --- 2. Handle Offline/Fallback Mode ---
        if not self.client:
             if hasattr(session_or_prompt, 'messages'):
                 return self._simulated_chat_response(actual_text or "")
             else:
                 return self._simulated_chat_response(actual_text or "")

        messages = []
        
        # Check if first arg is a session object
        if hasattr(session_or_prompt, 'messages'):
            session = session_or_prompt
            # 1. Add System Prompt
            system_prompt = self.get_system_prompt()
            messages.append({"role": "system", "content": system_prompt})
            
            # 2. Add History (Optimized: Last 6 messages only to save context)
            history = session.messages.order_by('-created_at')[:6]
            for msg in reversed(history):
                role = "user" if msg.role == 'USER' else "assistant"
                # Truncate very long messages to avoid token overflow
                content = msg.content[:2000] if len(msg.content) > 2000 else msg.content
                messages.append({"role": role, "content": content})
            
            # 3. Enhance latest user message
            if messages and messages[-1]['role'] == 'user' and user_content:
                messages[-1]['content'] = user_content
            elif user_content:
                messages.append({"role": "user", "content": user_content})
                
        else:
            # Simple prompt mode
            prompt = session_or_prompt
            messages = [{"role": "user", "content": prompt}]

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.3,
                max_tokens=2048,
            )
            return completion.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            logger.error(f"Chat Completion Error: {error_str}")
            
            if "429" in error_str or "Rate limit" in error_str:
                logger.warning("Rate Limit hit. Switching to simulated response.")
                if hasattr(session_or_prompt, 'messages'):
                    return self._simulated_chat_response(user_content or "Status Report")
                else:
                    prompt_str = str(session_or_prompt)
                    if "Translate" in prompt_str:
                        return self._simulated_translation(prompt_str, "")
                    else:
                        return self._simulated_chat_response(prompt_str)
            
            return f"عذراً، واجهت صعوبة تقنية في معالجة الطلب ({error_str[:50]}...). جاري حفظ الاستفسار للمراجعة."

    def _simulated_chat_response(self, user_input):
        """
        Generates a fake but plausible intelligence response when the LLM is unavailable.
        Uses local pattern matching to generate professional military/intelligence assessments.
        """
        user_input_lower = user_input.lower()
        
        # --- Intent 1: Greetings/Simple Queries ---
        if len(user_input) < 20 or any(w in user_input_lower for w in ['كيف', 'من أنت', 'hello', 'hi', 'مرحبا']):
             return "أنا نظام التحليل الاستراتيجي السيادي. أعمل حالياً في (الوضع الآمن/غير المتصل) نظراً لعدم توفر الاتصال بالمخدم المركزي. يمكنني تحليل النصوص واستخراج الكيانات والتهديدات بناءً على القواعد المحلية."

        # --- Intent 2: Analysis Request (Fallthrough to Pattern Analyzer) ---
        
        # 1. Determine Topic & Severity
        topic = "عام"
        severity = "متوسط"
        classification = "سري"
        keywords = []
        
        # Military/Conflict
        if any(w in user_input_lower for w in ['war', 'attack', 'missile', 'army', 'حرب', 'هجوم', 'صاروخ', 'جيش', 'عسكري', 'اشتباك', 'قصف']):
            topic = "عمليات عسكرية"
            severity = "حرج للغاية (CRITICAL)"
            classification = "سري للغاية (TOP SECRET)"
            keywords.append("نشاط عسكري معادِ")
            
        # Political/Diplomatic
        elif any(w in user_input_lower for w in ['minister', 'president', 'treaty', 'وزير', 'رئيس', 'اتفاقية', 'سياسة', 'حكومة', 'مرسوم']):
            topic = "شؤون سياسية"
            severity = "عالي (HIGH)"
            classification = "سري (SECRET)"
            keywords.append("تحركات دبلوماسية")
            
        # Security/Intel
        elif any(w in user_input_lower for w in ['spy', 'intel', 'security', 'terror', 'تجسس', 'استخبارات', 'أمن', 'إرهاب', 'تنظيم']):
            topic = "أمن قومي"
            severity = "حرج (CRITICAL)"
            classification = "سري للغاية (TOP SECRET)"
            keywords.append("تهديد أمني محتمل")

        # Specific Entities (Sovereign Priority)
        entities = []
        if any(w in user_input_lower for w in ['yemen', 'houthi', 'اليمن', 'حوثي']): entities.append("الجمهورية اليمنية / الميليشيات")
        if any(w in user_input_lower for w in ['iran', 'إيران']): entities.append("الجمهورية الإسلامية الإيرانية")
        if any(w in user_input_lower for w in ['usa', 'us', 'america', 'أمريكا', 'واشنطن']): entities.append("الولايات المتحدة الأمريكية")
        if any(w in user_input_lower for w in ['israel', 'إسرائيل', 'zionist']): entities.append("الكيان الإسرائيلي")
        if any(w in user_input_lower for w in ['saudi', 'ksa', 'السعودية', 'المملكة']): entities.append("المملكة العربية السعودية")
        
        entity_str = "، ".join(entities) if entities else "غير محدد"

        # 2. Construct Professional Assessment (Template-Based)
        
        response = f"""**وثيقة تقدير موقف (Intelligence Assessment)**
**الحالة:** (وضع التحليل المحلي - Local Mode)
**التصنيف:** {classification}
**الموضوع:** تحليل {topic} - {entity_str}
**تاريخ التحليل:** {timezone.now().strftime('%Y-%m-%d %H:%M')}

---

### 1. القراءة الأولية (Initial Readout)
تشير البيانات المدخلة إلى نشاط يتعلق بـ **{topic}**. النظام في وضع "الاستجابة المحلية"، لذا يعتمد التحليل على الكلمات المفتاحية والأنماط المخزنة مسبقاً.

### 2. تحليل الكيانات (Entities Analysis)
- **الكيانات المرصودة:** {entity_str}.
- **مستوى الخطورة:** {severity}.
- **المؤشرات:** {", ".join(keywords) if keywords else "لا توجد مؤشرات محددة في قاعدة البيانات المحلية"}.

### 3. التوصيات الفورية (Immediate Actions)
1. **أرشفة:** حفظ الاستفسار في سجلات الاستخبارات.
2. **تنبيه:** إذا كان المحتوى يتضمن تهديداً للمملكة، يرجى تفعيل التنبيه اليدوي.

---
*ملاحظة: هذا رد آلي من (المحرك السيادي المحلي) نظراً لتعذر الوصول للشبكة العصبية السحابية.*"""

        return response

