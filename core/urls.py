from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='root'),
    path('login/', views.SecurityLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/login/qr/', views.qr_login_view, name='qr_login'),
    path('card/<str:username>/', views.user_card_view, name='user_card'),
    path('audit/', views.audit_log_view, name='audit_log'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/add/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('password-reset/', views.password_reset_request_view, name='password_reset_request'),
]
