from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import AgentSession, AgentMessage, AgentDocument, AgentInstruction
from .services import GroqClient

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
    
    context = {
        'sessions': sessions,
        'active_session': active_session,
        'messages': messages,
    }
    return render(request, 'intelligence_agent/chat.html', context)

@login_required
def create_new_session(request):
    """Creates a new empty session."""
    session = AgentSession.objects.create(user=request.user, title="محادثة جديدة")
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
                # TODO: Implement PDF parsing using pypdf.
                # Requires: pip install pypdf
                # import pypdf
                # reader = pypdf.PdfReader(attachment)
                # text = ""
                # for page in reader.pages: text += page.extract_text()
                ai_context_content += f"\n\n[System: User uploaded PDF '{attachment.name}'. PDF parsing requires 'pypdf' library installation. Notify the user.]"
            else:
                ai_context_content += f"\n\n[System: User uploaded file '{attachment.name}'. File content analysis not fully supported yet, but acknowledge receipt.]"
        except Exception as e:
            ai_context_content += f"\n\n[System: Error reading file '{attachment.name}': {str(e)}]"

    # 2. Get AI Response
    client = GroqClient()
    ai_response_text = client.chat_completion(session, ai_context_content)
    
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
def agent_settings_view(request):
    """
    View to manage system prompts and uploaded documents.
    Restricted to ADMIN and MANAGER.
    """
    if request.user.role not in ['ADMIN', 'MANAGER'] and not request.user.is_superuser:
        raise PermissionDenied("Access Restricted to Managers and Admins")

    if request.method == 'POST':
        # Handle Instruction Update
        if 'update_instruction' in request.POST:
            prompt = request.POST.get('system_prompt')
            AgentInstruction.objects.update_or_create(
                id=1, # Simple singleton approach for now
                defaults={'name': 'Main Protocol', 'system_prompt': prompt}
            )
        
        # Handle File Upload
        if 'upload_document' in request.POST and request.FILES.get('document'):
            doc = request.FILES['document']
            AgentDocument.objects.create(
                title=doc.name,
                file=doc,
                uploaded_by=request.user
            )
            
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
