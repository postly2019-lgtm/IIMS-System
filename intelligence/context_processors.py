from django.utils import timezone
from datetime import timedelta
from django.db import connection
from .models import IntelligenceReport, Source, Entity

def global_status_context(request):
    """
    Provides global status indicators for the sidebar and other views.
    Ensures consistency across the application.
    """
    try:
        # Quick DB availability check (no retries here; middleware handles retries)
        connection.ensure_connection()
        db_available = True
    except Exception:
        db_available = False

    if not db_available:
        return {
            'recent_reports_count': 0,
            'ingestion_online': False,
            'analysis_online': False,
        }

    recent_reports_count = IntelligenceReport.objects.filter(
        published_at__gte=timezone.now() - timedelta(hours=24)
    ).count()
    ingestion_online = Source.objects.filter(is_active=True).exists()
    analysis_online = IntelligenceReport.objects.exists() 
    
    return {
        'recent_reports_count': recent_reports_count,
        'ingestion_online': ingestion_online,
        'analysis_online': analysis_online,
    }
