from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
from . import health_views

urlpatterns = [
    # Main routes
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='root'),
    path('login/', views.SecurityLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/login/qr/', views.qr_login_view, name='qr_login'),
    
    # User management
    path('card/<str:username>/', views.user_card_view, name='user_card'),
    path('audit/', views.audit_log_view, name='audit_log'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/add/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('password-reset/', views.password_reset_request_view, name='password_reset_request'),
    path('health/', health_views.health_check, name='health_check'),
    path('health/detailed/', health_views.detailed_health_check, name='detailed_health_check'),
    path('health/ready/', health_views.readiness_check, name='readiness_check'),
    path('health/live/', health_views.liveness_check, name='liveness_check'),
]
