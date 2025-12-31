from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.agent_chat_view, name='agent_chat_root'),
    path('chat/<int:session_id>/', views.agent_chat_view, name='agent_chat'),
    path('chat/new/', views.create_new_session, name='agent_new_session'),
    path('chat/<int:session_id>/send/', views.send_message, name='agent_send_message'),
    path('chat/<int:session_id>/delete/', views.delete_session, name='agent_delete_session'),
    path('settings/', views.agent_settings_view, name='agent_settings'),
    path('health/llm/', views.llm_health_check, name='llm_health_check'),
]
