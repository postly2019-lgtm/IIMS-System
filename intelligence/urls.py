from django.urls import path
from . import views, search_views, graph_views, source_views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('sources/', source_views.source_manager_view, name='source_manager'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('report/<int:report_id>/translate/', views.translate_report_api, name='translate_report'),
    path('report/<int:report_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/analyze/', views.analyze_favorites, name='analyze_favorites'),
    path('api/notifications/check/', views.check_notifications, name='check_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('search/', search_views.search_view, name='search'),
    path('search/fetch/', search_views.fetch_urls_view, name='fetch_urls'),
    path('graph/', views.graph_view, name='graph_view'),
    path('api/graph-data/', graph_views.graph_data_api, name='graph_data'),
    path('alerts/manage/', views.manage_alerts, name='manage_alerts'),
    path('alerts/delete/<int:rule_id>/', views.delete_alert_rule, name='delete_alert_rule'),
    path('alerts/analysis/<int:report_id>/', views.critical_analysis_view, name='critical_analysis'),
]
