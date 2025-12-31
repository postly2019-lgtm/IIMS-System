from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import AgentSession, AgentMessage, AgentDocument, AgentInstruction
from .services import GroqClient
from intelligence.models import IntelligenceReport
import os
from dotenv import set_key

@login_required
def agent_chat_view(request, session_id=None):
    """
    Main chat interface.
    """
    sessions = AgentSession.objects.filter(user=request.user).order_by('-last_interaction')
    
    active_session = None
    messages = []
    
    if session_id:
        active_session = get_object_or_404(AgentSession, id=session_id, user=request.user)
        messages = active_session.messages.all()
    elif sessions.exists():
        # Default to latest session
        active_session = sessions.first()
        messages = active_session.messages.all()
    else:
        # No sessions exist, create one immediately to ensure valid session_id
        active_session = AgentSession.objects.create(user=request.user, title="محادثة جديدة")
        messages = []
    
    context = {
        'sessions': sessions,
        'active_session': active_session,
        'messages': messages,
    }
    return render(request, 'intelligence_agent/chat.html', context)

@login_required
def create_new_session(request):
    """Creates a new empty session, optionally initialized with a report context."""
    report_id = request.GET.get('report_id')
    initial_title = "محادثة جديدة"
    
    if report_id:
        report = get_object_or_404(IntelligenceReport, pk=report_id)
        initial_title = f"تحليل: {report.title[:30]}..."
    
    session = AgentSession.objects.create(user=request.user, title=initial_title)
    
    if report_id:
        report = get_object_or_404(IntelligenceReport, pk=report_id)
        
        # System/User Context Injection - Natural Language
        user_content = f"قم بتحليل التقرير التالي: '{report.title}'"
        
        # Save User Message
        AgentMessage.objects.create(
            session=session,
            role=AgentMessage.Role.USER,
            content=user_content
        )
        
        # Trigger AI Response immediately
        client = GroqClient()
        
        # Add the report content as invisible system context or just part of the prompt
        # We append it to the user content for the AI to see, but maybe we don't need to save the HUGE text in the user message DB if we want to keep chat clean.
        # However, for RAG, it's better to have it.
        # Let's send the full content to the AI but only show the summary to the user? 
        # No, simpler is better. Send full content to AI.
        
        full_prompt = f"""{user_content}
        
[سياق التقرير]:
العنوان: {report.title}
المصدر: {report.source.name}
التاريخ: {report.published_at}
النص الكامل:
{report.content}
"""
        # Always attempt completion
        ai_response = client.chat_completion(session, full_prompt)
        
        AgentMessage.objects.create(
            session=session,
            role=AgentMessage.Role.ASSISTANT,
            content=ai_response
        )

    return redirect('agent_chat', session_id=session.id)

@login_required
@require_POST
def send_message(request, session_id):
    """
    API endpoint to handle user messages with optional attachments.
    """
    session = get_object_or_404(AgentSession, id=session_id, user=request.user)
    data = request.POST
    content = data.get('content', '').strip()
    attachment = request.FILES.get('attachment')
    
    if not content and not attachment:
        return JsonResponse({'error': 'No content or attachment'}, status=400)
    
    # Update title if it's the first message
    if session.messages.count() == 0:
        title_content = content if content else (attachment.name if attachment else "New Chat")
        session.title = title_content[:50] + "..."
        session.save()

    # 1. Save User Message
    user_msg = AgentMessage.objects.create(
        session=session,
        role=AgentMessage.Role.USER,
        content=content,
        attachment=attachment
    )

    # Prepare context for AI
    ai_context_content = content
    if attachment:
        try:
            # Simple text extraction for now. 
            # Ideally, use libraries like PyPDF2 or textract for robust parsing.
            if attachment.name.endswith('.txt') or attachment.name.endswith('.md') or attachment.name.endswith('.csv'):
                file_content = attachment.read().decode('utf-8', errors='ignore')
                ai_context_content += f"\n\n[System: User uploaded file '{attachment.name}'. Content:]\n{file_content}\n[End of file]"
            elif attachment.name.endswith('.pdf'):
                try:
                    import pypdf
                    # Reset pointer just in case, though usually at 0 for fresh upload
                    if hasattr(attachment, 'seek'):
                        attachment.seek(0)
                    
                    reader = pypdf.PdfReader(attachment)
                    text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                    
                    if not text.strip():
                        text = "[PDF contains no extractable text - might be an image scan]"

                    ai_context_content += f"\n\n[System: User uploaded PDF '{attachment.name}'. Content extracted below:]\n{text}\n[End of PDF]"
                except ImportError:
                    ai_context_content += f"\n\n[System: User uploaded PDF '{attachment.name}'. Error: pypdf library not installed on server.]"
                except Exception as e:
                    ai_context_content += f"\n\n[System: User uploaded PDF '{attachment.name}'. Error parsing PDF: {str(e)}]"
            else:
                ai_context_content += f"\n\n[System: User uploaded file '{attachment.name}'. File content analysis not fully supported yet, but acknowledge receipt.]"
        except Exception as e:
            ai_context_content += f"\n\n[System: Error reading file '{attachment.name}': {str(e)}]"

    # 2. Get AI Response
    client = GroqClient()
    
    # Check for report context (Active Context Injection)
    context_data = {}
    report_id = data.get('report_id')
    if report_id:
        context_data['report_id'] = report_id

    ai_response_text = client.chat_completion(session, ai_context_content, context_data=context_data)
    
    # 3. Save AI Message
    ai_message = AgentMessage.objects.create(
        session=session,
        role=AgentMessage.Role.ASSISTANT,
        content=ai_response_text
    )
    
    return JsonResponse({
        'status': 'success',
        'user_message': content,
        'attachment_url': user_msg.attachment.url if user_msg.attachment else None,
        'ai_message': ai_message.content,
        'created_at': ai_message.created_at.strftime('%H:%M')
    })

@login_required
@require_POST
def delete_session(request, session_id):
    """
    Deletes a specific chat session.
    """
    session = get_object_or_404(AgentSession, id=session_id, user=request.user)
    session.delete()
    return JsonResponse({'status': 'success', 'message': 'Session deleted'})

@login_required
def agent_settings_view(request):
    """
    View to manage system prompts and uploaded documents.
    Restricted to ADMIN and MANAGER.
    """
    if request.user.role not in ['ADMIN', 'MANAGER'] and not request.user.is_superuser:
        raise PermissionDenied("Access Restricted to Managers and Admins")

    if request.method == 'POST':
        # Handle API Key Update
        if 'update_api_key' in request.POST:
            new_key = request.POST.get('api_key', '').strip()
            if new_key:
                env_file = os.path.join(settings.BASE_DIR, '.env')
                # Ensure .env exists
                if not os.path.exists(env_file):
                    with open(env_file, 'w') as f:
                        f.write(f"GROQ_API_KEY={new_key}\n")
                else:
                    set_key(env_file, "GROQ_API_KEY", new_key)
                
                # Update runtime environment
                os.environ["GROQ_API_KEY"] = new_key
                settings.GROQ_API_KEY = new_key

        # Handle Instruction Update
        if 'update_instruction' in request.POST:
            prompt = request.POST.get('system_prompt')
            # Update active instruction or create if missing
            instruction = AgentInstruction.objects.filter(is_active=True).first()
            if not instruction:
                instruction = AgentInstruction.objects.first()
            
            if instruction:
                instruction.system_prompt = prompt
                instruction.save()
            else:
                AgentInstruction.objects.create(
                    name='Standard Protocol', 
                    system_prompt=prompt, 
                    is_active=True
                )
        
        # Handle File Upload
        if 'upload_document' in request.POST and request.FILES.get('document'):
            doc = request.FILES['document']
            agent_doc = AgentDocument.objects.create(
                title=doc.name,
                file=doc,
                uploaded_by=request.user,
                is_processed=False
            )
            
            # Process Document Immediately
            try:
                extracted_text = extract_text_from_file(doc)
                if extracted_text:
                    agent_doc.content_text = extracted_text
                    agent_doc.is_processed = True
                    agent_doc.save()
            except Exception as e:
                # Log error but keep document
                print(f"Error processing document {doc.name}: {e}")

        return redirect('agent_settings')

    instruction = AgentInstruction.objects.first()
    documents = AgentDocument.objects.filter(uploaded_by=request.user).order_by('-created_at')
    
    # Check if API Key is configured
    from django.conf import settings
    api_key_configured = bool(settings.GROQ_API_KEY)

    context = {
        'instruction': instruction,
        'documents': documents,
        'api_key_configured': api_key_configured
    }
    return render(request, 'intelligence_agent/settings.html', context)

def llm_health_check(request):
    """
    Health check endpoint for LLM connectivity.
    Sends a small prompt to the model and returns OK/FAIL.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        client = GroqClient()
        # Send a very small prompt to minimize cost/latency
        # Using chat_completion with a simple string prompt
        response = client.chat_completion("ping")
        
        if "⚠️" in response or "Error" in response:
             # Identify if it's a caught error in chat_completion
             raise Exception(response)
             
        return JsonResponse({"status": "OK", "message": "LLM Operational"})
    except Exception as e:
        error_msg = str(e)
        # Log the full error for debugging (ensure no API key leakage in simple string)
        logger.error(f"LLM Health Check Failed: {error_msg}")
        return JsonResponse({
            "status": "FAIL", 
            "reason": "LLM Connection Failed", 
            "details": error_msg[:200] # Truncate for security
        }, status=500)
