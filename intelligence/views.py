from django.shortcuts import render, get_object_or_404
from .models import IntelligenceReport, Source
from core.models import UserActionLog
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

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

def graph_view(request):
    return render(request, 'intelligence/graph.html', {})
