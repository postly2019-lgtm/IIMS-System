import os
import logging
import re
from django.conf import settings
from django.utils import timezone
from .models import AgentInstruction, AgentMessage, AgentSession, AgentDocument
from intelligence.models import IntelligenceReport
from django.db.models import Q

logger = logging.getLogger(__name__)

def extract_text_from_file(file_obj):
    """
    Extracts text from an uploaded file (PDF, TXT, MD, CSV, JSON).
    Returns a string containing the extracted text or an error message.
    """
    try:
        # Reset pointer
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
            
        filename = file_obj.name.lower()
        extracted_text = ""

        if filename.endswith('.pdf'):
            try:
                import pypdf
                reader = pypdf.PdfReader(file_obj)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
                
                if not extracted_text.strip():
                    return "[PDF contains no extractable text - might be an image scan]"
            except ImportError:
                return "[System Error: pypdf library not installed on server]"
            except Exception as e:
                return f"[Error extracting PDF: {str(e)}]"

        elif filename.endswith(('.txt', '.md', '.csv', '.json')):
            try:
                extracted_text = file_obj.read().decode('utf-8', errors='ignore')
            except Exception as e:
                return f"[Error reading text file: {str(e)}]"
        else:
            return f"[File type '{filename}' not fully supported for text extraction]"

        return extracted_text if extracted_text else "[File is empty]"

    except Exception as e:
        return f"[General Error reading file: {str(e)}]"

class GroqClient:
    def __init__(self):
        try:
            from groq import Groq
            api_key = settings.GROQ_API_KEY
            if not api_key:
                logger.error("CRITICAL: GROQ_API_KEY is not set. AI features disabled.")
                self.client = None
            else:
                self.client = Groq(api_key=api_key)
        except ImportError:
            logger.error("Groq SDK not installed.")
            self.client = None

    def _call_groq(self, messages, temperature=0.3, max_tokens=4096, model=None):
        """
        Executes Groq API call with fallback logic for decommissioned models.
        """
        if not self.client:
            raise Exception("Groq Client not initialized")

        primary_model = model or settings.GROQ_MODEL
        fallback_model = "llama-3.3-70b-versatile"
        
        try:
            return self.client.chat.completions.create(
                model=primary_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=False,
                stop=None
            )
        except Exception as e:
            error_msg = str(e)
            if "model_decommissioned" in error_msg or "not found" in error_msg:
                logger.warning(f"Model {primary_model} decommissioned/failed. Retrying with fallback {fallback_model}...")
                try:
                    return self.client.chat.completions.create(
                        model=fallback_model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=1,
                        stream=False,
                        stop=None
                    )
                except Exception as fallback_error:
                    logger.error(f"Fallback model failed: {fallback_error}")
                    raise fallback_error
            else:
                raise e


    def get_system_prompt(self):
        """Retrieve the active system prompt or use the Sovereign Standard."""
        # Use active instructions first
        instruction = AgentInstruction.objects.filter(is_active=True).first()
        if instruction:
            return instruction.system_prompt
            
        # SOVEREIGN INTELLIGENCE STANDARD PROMPT (ARABIC ONLY)
        return """SYSTEM PROMPT — SOVEREIGN ARABIC INTELLIGENCE AGENT (PREMIUM)

You are a Senior Sovereign Intelligence Systems Architect and Analytical Agent with more than 20 years of experience designing and operating high-security intelligence, security operations, and decision-support platforms for government-level and critical infrastructure environments.

You do NOT behave as a general assistant.
You operate as an intelligence system component.

Your mission is to collect, normalize, analyze, correlate, evaluate credibility, and support decision-making in high-risk environments — exclusively in Arabic.

ABSOLUTE OPERATING RULES (NON-NEGOTIABLE)

Arabic-Only Output

ALL outputs, reports, summaries, dashboards, alerts, and explanations MUST be in Modern Standard Arabic.

Full RTL logic is mandatory.

English is FORBIDDEN in final outputs (except source names or proper nouns when required).

Mandatory Content Arabization

ANY non-Arabic content (articles, posts, reports, social media, data) MUST be:

Interpreted

Translated into Arabic

Contextually adapted (not literal translation)

Preserved with original meaning and intelligence nuance

The original language may be retained internally for traceability ONLY.

Intelligence Thinking Protocol (MANDATORY ORDER)
You MUST ALWAYS follow this sequence before producing conclusions:

ANALYZE → THINK DEEPLY → DECIDE → VERIFY → REPORT

Never skip a stage

Never merge stages

Never output conclusions without verification

No Assumptions Without Evidence

Every claim must be supported by:

Source references

Cross-source confirmation

Or clearly labeled confidence levels

No Feature Drift

Do NOT add functionality, speculation, opinions, or creative output unless explicitly requested.

You operate strictly within intelligence and analysis scope.

CORE INTELLIGENCE MINDSET

Treat ALL data as potentially sensitive

Assume hostile, misleading, or manipulated information is possible

Prioritize signal over noise

Focus on decision impact, not verbosity

Favor structured, verifiable, and explainable reasoning

ARABIC INTELLIGENCE LANGUAGE GOVERNANCE

Use standardized Arabic terminology for:

Security

Intelligence

Politics

Economics

Military

Technology

Normalize Arabic text:

Remove diacritics for analysis

Normalize letter variants (أ / إ / آ → ا)

Support name variants and aliases

Perform Arabic entity extraction:

Persons

Organizations

Locations

Events

Dates

Assets

INTELLIGENCE DATA HANDLING
Data Sources

You may process data from:

RSS feeds

APIs

Authorized websites

Reports and documents

Social media platforms ONLY via legal, authorized, or provided connectors

Scraping or policy-violating collection is STRICTLY FORBIDDEN.

Processing Pipeline (REQUIRED)

Every piece of information MUST pass through:

Source identification

Language detection

Arabic translation & contextualization

De-duplication

Entity extraction

Event correlation

Credibility scoring

Impact assessment

CREDIBILITY & TRUST SCORING (MANDATORY)

For every article, post, or claim, generate a numerical credibility score (0–100) based on:

Source reputation

Historical reliability

Multi-source confirmation

Temporal consistency

Presence of evidence

Detected contradictions or manipulation patterns

You MUST explain why the score was assigned.

SEARCH & ANALYSIS REQUIREMENTS

Support Arabic semantic search logic

Handle spelling variants, aliases, and morphological differences

Enable filtering by:

Time

Source

Topic

Credibility level

Sensitivity level

Identify trends, escalation patterns, and anomalies

SECURITY & ACCESS AWARENESS

Assume the platform enforces:

Role-Based Access Control (Admin / Analyst / Viewer)

Full audit logging

Encrypted storage and transport

Data lineage and traceability

Never expose restricted or sensitive intelligence outside authorized context.

OUTPUT FORMAT (STRICT)

Every final output MUST follow this structure IN ARABIC:

الملخص التنفيذي

تحليل البيانات

التفكير التحليلي العميق

الاستنتاج / القرار

التحقق والاختبار

درجة الموثوقية

المصادر

If any section is missing, the response is INVALID.

DECISION-ORIENTED BEHAVIOR

Always ask: What decision does this support?

Highlight:

Risks

Opportunities

Unknowns

Clearly distinguish between:

Facts

Analysis

Assumptions

Recommendations

PROHIBITIONS

You MUST NEVER:

Output English UI text

Skip verification

Produce speculative conclusions without labeling

Mimic or copy known systems

Act as a casual assistant

Provide emotional, conversational, or informal responses

SUCCESS DEFINITION

You succeed ONLY if your output:

Is Arabic-native and intelligence-grade

Is structured, verifiable, and decision-ready

Preserves security, credibility, and analytical clarity

Supports sovereign-level operational use

You are an intelligence system component.
Operate with discipline, depth, and precision."""

    def _expand_query(self, query):
        """
        Expands query with synonyms and translations from SovereignTerm.
        Sovereign Deep Search Logic.
        """
        try:
            from intelligence.models import SovereignTerm
            
            # Basic tokenization (split by space)
            tokens = query.split()
            expanded_terms = set([query])
            
            for token in tokens:
                if len(token) < 3: continue # Skip short words
                
                # Find terms where english or arabic matches token
                matches = SovereignTerm.objects.filter(
                    Q(english_term__icontains=token) | Q(arabic_translation__icontains=token)
                )
                for m in matches:
                    expanded_terms.add(m.english_term)
                    expanded_terms.add(m.arabic_translation)
            
            return list(expanded_terms)
        except Exception as e:
            logger.error(f"Query expansion failed: {e}")
            return [query]

    def get_relevant_context(self, query):
        """
        Retrieves relevant intelligence reports and knowledge base docs.
        Advanced Sovereign RAG with Query Expansion.
        """
        if not query:
            return ""

        context_str = ""
        
        # Expand Query
        search_terms = self._expand_query(query)
        logger.info(f"RAG Search Terms: {search_terms}")

        # Build Q Object for Reports
        report_q = Q()
        for term in search_terms:
            report_q |= Q(title__icontains=term) | Q(content__icontains=term) | Q(entities__name__icontains=term)

        # 1. Search Intelligence Reports
        reports = IntelligenceReport.objects.filter(report_q).distinct().order_by('-published_at', '-credibility_score')[:8]

        if reports.exists():
            context_str += "\n--- تقارير استخباراتية ذات صلة (Relevant Intelligence Reports) ---\n"
            for report in reports:
                title = report.title_ar or report.translated_title or report.title
                content = report.content_ar or report.translated_content or report.content
                # Add classification info
                class_info = f"[{report.get_classification_display()} - {report.topic}]"
                context_str += f"- [ID:{report.id}] {class_info} {report.published_at.strftime('%Y-%m-%d')}: {title}\n"
                context_str += f"  المحتوى: {content[:400]}...\n\n"

        # 2. Search Agent Documents (Knowledge Base)
        # Build Q Object for Docs
        doc_q = Q()
        for term in search_terms:
            doc_q |= Q(title__icontains=term) | Q(content_text__icontains=term)

        docs = AgentDocument.objects.filter(doc_q).filter(is_processed=True).distinct().order_by('-created_at')[:3]

        if docs.exists():
            context_str += "\n--- قاعدة المعرفة (Knowledge Base) ---\n"
            for doc in docs:
                # Simple snippet extraction around the keyword could be better, but truncating is safe for now
                snippet = doc.content_text[:500]
                context_str += f"- [Doc: {doc.title}]\n{snippet}...\n\n"

        return context_str

    def translate_with_chunking(self, text, is_title=False):
        """
        Translates text using the user-specified sovereign prompt with chunking.
        """
        if not text:
            return ""

        if not self.client:
            logger.warning("GroqClient not initialized. Translation skipped.")
            return None

        # Fixed Sovereign Prompt
        system_prompt = "ترجم إلى العربية الفصحى مع الحفاظ على الأسماء والأرقام كما هي. لا تضف معلومات."

        # If title or short text, translate directly
        if is_title or len(text) < 4000:
            try:
                completion = self._call_groq(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.3
                )
                return completion.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"Translation Error: {e}")
                return None

        # Chunking for long content
        chunk_size = 4000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        translated_chunks = []
        
        for chunk in chunks:
            try:
                completion = self._call_groq(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chunk}
                    ],
                    temperature=0.3
                )
                translated_chunks.append(completion.choices[0].message.content.strip())
            except Exception as e:
                logger.error(f"Chunk Translation Error: {e}")
                # Fallback: append original chunk if translation fails to avoid data loss
                translated_chunks.append(chunk)

        return "\n".join(translated_chunks)

    def translate_report_obj(self, report):
        """
        Translates an IntelligenceReport object and saves it.
        """
        if report.processing_status == 'COMPLETED' and report.translated_title:
            return True

        if not self.client:
            # Fallback for offline/demo - DO NOT USE BAD SIMULATION
            # Just keep original text but mark as processed to avoid "weird symbols"
            if not report.translated_title:
                report.translated_title = report.title + " (Offline Mode)"
                report.translated_content = report.content
                report.processing_status = 'COMPLETED'
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
        Translates text to Arabic using the LLM.
        """
        if not self.client:
            logger.warning("GroqClient not initialized. Translation skipped.")
            return None # No simulation allowed

        prompt = f"""
        ترجم إلى العربية الفصحى مع الحفاظ على الأسماء والأرقام كما هي. لا تضف معلومات.
        
        العنوان: {title}
        المحتوى: {content}
        
        Output Format:
        Title: [Arabic Title]
        Content: [Arabic Content]
        """

        try:
            completion = self._call_groq(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=4096,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Translation Error: {e}")
            return None

    def chat_completion(self, session_or_prompt, user_content=None, context_data=None):
        """
        Wrapper for chat completion that handles both simple prompts and full session context.
        Supports 'context_data' to inject specific report details.
        """
        # Resolve actual user text
        actual_text = user_content
        if not actual_text and not hasattr(session_or_prompt, 'messages'):
            actual_text = str(session_or_prompt)

        # --- Strict Real Mode: No Simulation ---
        if not self.client:
            return "⚠️ خطأ في النظام: لا يمكن الاتصال بمحرك الذكاء الاصطناعي (Groq Client Not Initialized)."

        messages = []
        
        # Check if first arg is a session object
        if hasattr(session_or_prompt, 'messages'):
            session = session_or_prompt
            
            # 1. Add System Prompt
            system_prompt = self.get_system_prompt()
            messages.append({"role": "system", "content": system_prompt})
            
            # 1.0 Inject Direct Context (If User is viewing a specific report)
            if context_data and context_data.get('report_id'):
                try:
                    report = IntelligenceReport.objects.get(id=context_data['report_id'])
                    report_context = f"""
                    ** Active Intelligence Report Context **
                    You are currently analyzing this specific report. All answers should reference it.
                    Title: {report.translated_title or report.title}
                    Classification: {report.get_classification_display()} / {report.severity}
                    Content: {report.translated_content or report.content}
                    """
                    messages.append({"role": "system", "content": report_context})
                    logger.info(f"Injected context for Report ID: {report.id}")
                except IntelligenceReport.DoesNotExist:
                    pass

            # 1.1 Add RAG Context (General Search)
            rag_context = self.get_relevant_context(actual_text)
            if rag_context:
                messages.append({"role": "system", "content": f"Use this broader knowledge base if relevant:\n{rag_context}"})
            
            # 2. Add History (Last 10 messages)
            history = session.messages.order_by('-created_at')[:10]
            for msg in reversed(history):
                role = "user" if msg.role == 'USER' else "assistant"
                content = msg.content[:4000] if len(msg.content) > 4000 else msg.content
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
            # Use _call_groq wrapper
            completion = self._call_groq(
                messages=messages,
                temperature=0.3,
                max_tokens=4096,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq Chat Error: {e}")
            return f"⚠️ حدث خطأ أثناء الاتصال بالنموذج الذكي: {str(e)}"

