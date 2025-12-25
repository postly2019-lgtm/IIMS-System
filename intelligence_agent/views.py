from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import AgentSession, AgentMessage, AgentDocument, AgentInstruction
from .services import AIService

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
    API endpoint to handle user messages.
    """
    session = get_object_or_404(AgentSession, id=session_id, user=request.user)
    data = request.POST
    content = data.get('content')
    
    if not content:
        return JsonResponse({'error': 'No content'}, status=400)
    
    # Update title if it's the first message
    if session.messages.count() == 0:
        session.title = content[:50] + "..."
        session.save()

    service = AIService()
    ai_message = service.generate_response(session, content)
    
    return JsonResponse({
        'status': 'success',
        'user_message': content,
        'ai_message': ai_message.content,
        'created_at': ai_message.created_at.strftime('%H:%M')
    })

@login_required
def agent_settings_view(request):
    """
    View to manage system prompts and uploaded documents.
    """
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
    
    context = {
        'instruction': instruction,
        'documents': documents
    }
    return render(request, 'intelligence_agent/settings.html', context)
