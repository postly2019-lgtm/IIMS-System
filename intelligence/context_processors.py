from .models import IntelligenceReport, Source, Entity
from django.utils import timezone
from datetime import timedelta

def global_status_context(request):
    """
    Provides global status indicators for the sidebar and other views.
    Ensures consistency across the application.
    """
    # 24h Reports Count
    recent_reports_count = IntelligenceReport.objects.filter(
        published_at__gte=timezone.now() - timedelta(hours=24)
    ).count()

    # Ingestion Status: Online if any source is active
    ingestion_online = Source.objects.filter(is_active=True).exists()

    # Analysis Status: Online if there are any entities OR any reports
    # (Making it more permissive so it doesn't show OFF just because no entities were found yet)
    analysis_online = IntelligenceReport.objects.exists() 
    
    return {
        'recent_reports_count': recent_reports_count,
        'ingestion_online': ingestion_online,
        'analysis_online': analysis_online,
    }
