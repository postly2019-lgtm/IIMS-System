from django.shortcuts import render, get_object_or_404, redirect
from .models import IntelligenceReport, Source
from core.models import UserActionLog
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from intelligence_agent.services import GroqClient
from django.contrib import messages
import logging

logger = logging.getLogger('intelligence')


def _log_with_request(request, level, message):
    """Helper to log with request ID context"""
    log_record = logger.makeRecord(
        logger.name, level, '', 0, message, (), None
    )
    log_record.request_id = getattr(request, 'request_id', 'no-request-id')
    logger.handle(log_record)

@login_required
@require_POST
def translate_report_api(request, report_id):
    """
    Translates a report using the AI Agent logic (Groq) via API (AJAX).
    """
    report = get_object_or_404(IntelligenceReport, pk=report_id)

    _log_with_request(
        request, logging.INFO,
        f"Translation requested for report {report_id} by user {request.user.username}"
    )

    # Return cached translation if available
    if report.translated_title and report.translated_content:
        _log_with_request(
            request, logging.INFO,
            f"Returning cached translation for report {report_id}"
        )
        return JsonResponse({
            'status': 'success',
            'title': report.translated_title,
            'content': report.translated_content
        })

    # Perform Translation via Groq
    client = GroqClient()
    if not client.client:
        _log_with_request(
            request, logging.ERROR,
            f"AI service unavailable for translation of report {report_id}"
        )
        return JsonResponse({'status': 'error', 'message': 'AI Service Unavailable (No API Key)'}, status=503)

    try:
        translation = client.translate_text(report.title, report.content)
        
        if translation:
            # Parse the output (Simple parsing assuming the model follows instructions)
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
            
            _log_with_request(
                request, logging.INFO,
                f"Successfully translated report {report_id}"
            )
            
            return JsonResponse({
                'status': 'success',
                'title': ar_title,
                'content': ar_content
            })
        
        _log_with_request(
            request, logging.ERROR,
            f"Translation failed for report {report_id}: Invalid output"
        )
        return JsonResponse({'status': 'error', 'message': 'Translation failed to generate valid output'}, status=500)

    except Exception as e:
        _log_with_request(
            request, logging.ERROR,
            f"Translation exception for report {report_id}: {str(e)}"
        )
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def dashboard_view(request):
    from django.db.models import Case, When, IntegerField
    
    # Define Priority Order
    # 1. Military, 2. Security, 3. Armament, 4. Intel, 5. Mil_Tech, 6. Medical (High Sev), 7. Others
    
    reports = IntelligenceReport.objects.select_related('source').prefetch_related('entities').annotate(
        priority_score=Case(
            When(topic='MILITARY', then=1),
            When(topic='SECURITY', then=2),
            When(topic='ARMAMENT', then=3),
            When(topic='INTEL', then=4),
            When(topic='MIL_TECH', then=5),
            When(topic='MEDICAL', severity__in=['HIGH', 'CRITICAL'], then=6),
            When(topic='MEDICAL', then=99), # Low priority medical
            default=7,
            output_field=IntegerField(),
        )
    ).order_by('priority_score', '-published_at')

    recent_reports = reports[:20]
    total_reports = IntelligenceReport.objects.count()
    sources_count = Source.objects.filter(is_active=True).count()
    
    # Calculate Critical Alerts Count (Unread Critical Notifications)
    from .models import IntelligenceNotification
    # Assuming the current user is the one viewing the dashboard. 
    # If notifications are per-user, we filter by request.user. 
    # But dashboard might show system-wide stats? 
    # Let's show unread critical notifications for the current user.
    critical_alerts_count = IntelligenceNotification.objects.filter(
        user=request.user, 
        level='CRITICAL', 
        is_read=False
    ).count()

    # Get Top Threats (High/Critical Severity) for the Ticker
    top_threats = IntelligenceReport.objects.filter(severity__in=['HIGH', 'CRITICAL']).order_by('-published_at')[:5]

    context = {
        'recent_reports': recent_reports,
        'total_reports': total_reports,
        'sources_count': sources_count,
        'critical_alerts_count': critical_alerts_count,
        'top_threats': top_threats,
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

@login_required
@require_POST
def toggle_favorite(request, report_id):
    report = get_object_or_404(IntelligenceReport, pk=report_id)
    if request.user in report.favorites.all():
        report.favorites.remove(request.user)
        is_favorite = False
    else:
        report.favorites.add(request.user)
        is_favorite = True
    
    return JsonResponse({'status': 'success', 'is_favorite': is_favorite})

@login_required
def manage_alerts(request):
    """
    Manage Critical Alert Rules.
    """
    from .models import CriticalAlertRule
    
    if request.method == 'POST':
        name = request.POST.get('name')
        keywords = request.POST.get('keywords')
        region = request.POST.get('region')
        
        if name and keywords:
            CriticalAlertRule.objects.create(
                user=request.user,
                name=name,
                keywords=keywords,
                region=region,
                severity_level='CRITICAL' # Default for now
            )
            messages.success(request, "تم إضافة قاعدة التنبيه بنجاح")
        return redirect('manage_alerts')
        
    rules = CriticalAlertRule.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'intelligence/manage_alerts.html', {'rules': rules})

@login_required
def delete_alert_rule(request, rule_id):
    from .models import CriticalAlertRule
    rule = get_object_or_404(CriticalAlertRule, pk=rule_id, user=request.user)
    rule.delete()
    messages.success(request, "تم حذف قاعدة التنبيه")
    return redirect('manage_alerts')

@login_required
def critical_analysis_view(request, report_id):
    """
    Special view for Critical Alerts.
    Triggers AI analysis immediately.
    """
    report = get_object_or_404(IntelligenceReport, pk=report_id)
    
    # 1. Check if we already have a cached analysis (e.g. in translated_content or separate field)
    # For now, we generate fresh or use existing translation if valid, 
    # but the user wants "Situation Analysis", not just translation.
    
    client = GroqClient()
    
    # Prompt for Critical Analysis
    prompt = f"""
    You are a Senior Strategic Intelligence Analyst.
    URGENT SITUATION REPORT REQUIRED.
    
    Subject: {report.title}
    Raw Intel: {report.content}
    
    Task: Provide a Critical Situation Assessment in ARABIC.
    Structure:
    1. **Strategic Significance** (Why this matters now)
    2. **Threat Assessment** (Who is threatened, severity)
    3. **Immediate Implications** (What will happen next 24-48h)
    4. **Recommendations** (Actionable steps)
    
    Tone: Urgent, Military, Professional.
    Language: Arabic.
    """
    
    if client.client:
        analysis = client.chat_completion(prompt)
    else:
        # Simulation Mode
        analysis = f"""
### تقدير موقف استراتيجي (عاجل)
**الموضوع:** {report.title}

1. **الأهمية الاستراتيجية:**
يشير هذا التقرير إلى تطور نوعي في {report.topic if report.topic else 'المنطقة'}. البيانات الأولية تؤكد وجود نشاط غير اعتيادي يتطلب الانتباه الفوري.

2. **تقييم التهديد:**
مستوى الخطورة: **مرتفع**. التهديدات تطال المصالح الحيوية، مع احتمالية تصعيد في غضون الساعات القادمة.

3. **التداعيات المباشرة:**
- توقع ردود فعل سياسية وعسكرية سريعة.
- احتمالية تغيير في قواعد الاشتباك الحالية.

4. **التوصيات:**
- رفع درجة التأهب في القطاعات ذات الصلة.
- تكثيف عمليات الرصد الاستخباراتي للمصادر المرتبطة بـ "{report.source.name}".

*تحليل تم إنشاؤه بواسطة المحلل الذكي للنظام.*
"""

    context = {
        'report': report,
        'analysis': analysis,
    }
    return render(request, 'intelligence/critical_analysis.html', context)
    return JsonResponse({'status': 'success', 'is_favorite': is_favorite})

@login_required
def favorites_list(request):
    favorite_reports = request.user.favorite_reports.all().order_by('-created_at')
    return render(request, 'intelligence/favorites_list.html', {'favorite_reports': favorite_reports})

@login_required
@require_POST
def analyze_favorites(request):
    try:
        import json
        data = json.loads(request.body)
        report_ids = data.get('report_ids', [])
        
        _log_with_request(
            request, logging.INFO,
            f"User {request.user.username} requested analysis of {len(report_ids)} reports"
        )
        
        if not report_ids:
            return JsonResponse({'status': 'error', 'message': 'No reports selected'})
            
        reports = IntelligenceReport.objects.filter(id__in=report_ids)
        if not reports.exists():
             return JsonResponse({'status': 'error', 'message': 'Reports not found'})

        # Prepare data for AI
        reports_data = [
            {'title': r.title, 'content': r.content, 'source': r.source.name}
            for r in reports
        ]
        
        client = GroqClient()
        analysis = client.analyze_reports(reports_data)
        
        _log_with_request(
            request, logging.INFO,
            f"Successfully analyzed {len(report_ids)} reports for user {request.user.username}"
        )
        
        return JsonResponse({'status': 'success', 'analysis': analysis})
    except Exception as e:
        _log_with_request(
            request, logging.ERROR,
            f"Analysis error for user {request.user.username}: {str(e)}"
        )
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def check_notifications(request):
    """
    API to return unread notifications count.
    """
    from .models import IntelligenceNotification
    count = IntelligenceNotification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'status': 'success', 'count': count})

@login_required
def mark_notification_read(request, notification_id):
    from .models import IntelligenceNotification
    try:
        notif = IntelligenceNotification.objects.get(id=notification_id, user=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({'status': 'success'})
    except IntelligenceNotification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

@login_required
def export_report(request, report_id):
    """
    Sovereign Export Functionality with Audit Logging.
    """
    report = get_object_or_404(IntelligenceReport, pk=report_id)
    
    # Security Audit
    UserActionLog.objects.create(
        user=request.user,
        action=UserActionLog.ActionType.EXPORT,
        target_object=f"Report ID: {report.id}",
        details=f"Exported report: {report.title}",
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Generate Simple Text Export
    response_content = f"""
    TOP SECRET // SOVEREIGN INTELLIGENCE SYSTEM
    -------------------------------------------
    Report ID: {report.id}
    Title: {report.title}
    Date: {report.published_at}
    Source: {report.source.name}
    Classification: {report.get_classification_display()}
    
    Content:
    {report.content}
    
    -------------------------------------------
    Exported by: {request.user.username}
    Date: {timezone.now()}
    IP: {request.META.get('REMOTE_ADDR')}
    """
    
    from django.http import HttpResponse
    response = HttpResponse(response_content, content_type="text/plain")
    response['Content-Disposition'] = f'attachment; filename="report_{report.id}_secure.txt"'
    return response

@login_required
def check_notifications(request):
    """
    Returns unread critical notifications for the polling script.
    """
    from .models import IntelligenceNotification
    notifications = IntelligenceNotification.objects.filter(
        user=request.user, 
        is_read=False, 
        level='CRITICAL'
    ).order_by('-created_at')
    
    if not notifications.exists():
        return JsonResponse({'status': 'ok', 'count': 0})
        
    data = []
    for notif in notifications:
        data.append({
            'id': notif.id,
            'title': notif.title,
            'message': notif.message,
            'level': notif.level,
            'report_id': notif.report.id if notif.report else None
        })
        
    return JsonResponse({'status': 'alert', 'count': notifications.count(), 'notifications': data})

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    from .models import IntelligenceNotification
    notif = get_object_or_404(IntelligenceNotification, pk=notification_id, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'success'})