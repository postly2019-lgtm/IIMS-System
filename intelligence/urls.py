from django.urls import path
from . import views, search_views, graph_views, source_views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('sources/', source_views.source_manager_view, name='source_manager'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('search/', search_views.search_view, name='search'),
    path('search/fetch/', search_views.fetch_urls_view, name='fetch_urls'),
    path('graph/', views.graph_view, name='graph_view'),
    path('api/graph-data/', graph_views.graph_data_api, name='graph_data'),
]
