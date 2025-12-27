from django.shortcuts import render, get_object_or_404
from .models import IntelligenceReport, Source
from core.models import UserActionLog
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from intelligence_agent.services import GroqClient
import logging

logger = logging.getLogger(__name__)

@login_required
@require_POST
def translate_report(request, report_id):
    """
    Translates a report using the AI Agent logic (Groq).
    """
    report = get_object_or_404(IntelligenceReport, pk=report_id)

    # Return cached translation if available
    if report.translated_title and report.translated_content:
        return JsonResponse({
            'status': 'success',
            'title': report.translated_title,
            'content': report.translated_content
        })

    # Perform Translation via Groq
    client = GroqClient()
    if not client.client:
        return JsonResponse({'status': 'error', 'message': 'AI Service Unavailable (No API Key)'}, status=503)

    prompt = f"""
    Translate the following Intelligence Report into professional Arabic.
    Maintain military and political terminology.
    
    Title: {report.title}
    Content: {report.content}
    
    Output Format:
    Title: [Arabic Title]
    Content: [Arabic Content]
    """
    
    try:
        # We use a temporary session-less call or just reuse chat_completion with a dummy object if needed, 
        # but GroqClient structure is tied to sessions. Let's make a raw call using the client directly if possible 
        # or adapt GroqClient.
        # Actually, GroqClient.chat_completion needs a session.
        # Let's instantiate Groq directly here for simplicity or add a helper method to GroqClient.
        # I'll add a helper method `translate_text` to GroqClient first to keep it clean.
        
        # Checking GroqClient in services.py... it has self.client.
        # I will assume I can use client.client.chat.completions.create directly here for now to avoid editing services.py yet again if not needed.
        # But wait, better to encapsulate. Let's add `translate_text` to GroqClient.
        
        # Re-reading services.py content from memory... 
        # It has `chat_completion(self, session, user_message_content)`.
        
        # Let's just use the raw client here for speed, or better, add the method. 
        # Adding the method is cleaner.
        pass
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # Let's implement the logic assuming I'll update services.py
    translation = client.translate_text(report.title, report.content)
    
    if translation:
        # Parse the output (Simple parsing assuming the model follows instructions)
        # Fallback: if parsing fails, just put everything in content.
        
        lines = translation.strip().split('\n')
        ar_title = ""
        ar_content = ""
        
        mode = "none"
        for line in lines:
            if line.startswith("Title:") or line.startswith("العنوان:"):
                ar_title = line.split(":", 1)[1].strip()
                mode = "title"
            elif line.startswith("Content:") or line.startswith("المحتوى:"):
                ar_content = line.split(":", 1)[1].strip()
                mode = "content"
            else:
                if mode == "content":
                    ar_content += "\n" + line
                elif mode == "title":
                    ar_title += " " + line
        
        if not ar_title: 
             ar_title = translation[:100] + "..."
        if not ar_content:
             ar_content = translation

        report.translated_title = ar_title
        report.translated_content = ar_content
        report.save()
        
        return JsonResponse({
            'status': 'success',
            'title': ar_title,
            'content': ar_content
        })
    
    return JsonResponse({'status': 'error', 'message': 'Translation failed'}, status=500)

@login_required
def dashboard_view(request):
    recent_reports = IntelligenceReport.objects.all()[:20]
    total_reports = IntelligenceReport.objects.count()
    sources_count = Source.objects.filter(is_active=True).count()
    recent_reports_count = IntelligenceReport.objects.filter(published_at__gte=timezone.now() - timedelta(hours=24)).count()
    ingestion_online = Source.objects.filter(is_active=True).exists()
    analysis_online = IntelligenceReport.objects.filter(entities__isnull=False).exists()
    
    context = {
        'recent_reports': recent_reports,
        'total_reports': total_reports,
        'sources_count': sources_count,
    }
    return render(request, 'intelligence/dashboard.html', context)

def report_detail(request, report_id):
    report = get_object_or_404(IntelligenceReport, pk=report_id)
    
    # Audit Log
    if request.user.is_authenticated:
        UserActionLog.objects.create(
            user=request.user,
            action=UserActionLog.ActionType.VIEW_REPORT,
            target_object=f"Report ID: {report.id}",
            details=f"Viewed report: {report.title}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
    
    context = {
        'report': report,
    }
    return render(request, 'intelligence/report_detail.html', context)

@login_required
def graph_view(request):
    return render(request, 'intelligence/graph.html', {})
