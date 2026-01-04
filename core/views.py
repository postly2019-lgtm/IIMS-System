from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from .models import UserActionLog
from .forms import UserForm
import json
import logging

# Get logger for this module
logger = logging.getLogger('core')


def _log_with_request(request, level, message):
    """Helper to log with request ID context"""
    log_record = logger.makeRecord(
        logger.name, level, '', 0, message, (), None
    )
    log_record.request_id = getattr(request, 'request_id', 'no-request-id')
    logger.handle(log_record)


class SecurityLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_ip'] = self.get_client_ip()
        return context
    
    def form_valid(self, form):
        # Log successful login
        response = super().form_valid(form)
        user = self.request.user
        ip = self.get_client_ip()
        
        _log_with_request(
            self.request, logging.INFO,
            f"User {user.username} successfully logged in from IP {ip}"
        )
        
        UserActionLog.objects.create(
            user=user,
            action=UserActionLog.ActionType.LOGIN,
            target_object="System Login",
            details="Successful login via password",
            ip_address=ip
        )
        return response

    def form_invalid(self, form):
        # Log failed attempt
        username = form.data.get('username')
        User = get_user_model()
        ip = self.get_client_ip()
        
        _log_with_request(
            self.request, logging.WARNING,
            f"Failed login attempt for username '{username}' from IP {ip}"
        )
        
        try:
            if username:
                user = User.objects.get(username=username)
                UserActionLog.objects.create(
                    user=user,
                    action=UserActionLog.ActionType.ACCESS_DENIED,
                    target_object="Login Failed",
                    details="Failed password attempt",
                    ip_address=ip
                )
        except User.DoesNotExist:
            pass
            
        return super().form_invalid(form)

def user_card_view(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    
    context = {
        'card_user': user,
    }
    return render(request, 'core/card.html', context)

@user_passes_test(lambda u: u.is_staff)
def audit_log_view(request):
    logs = UserActionLog.objects.all()[:100]
    return render(request, 'core/audit_log.html', {'logs': logs})

@user_passes_test(lambda u: u.is_staff)
def user_list_view(request):
    User = get_user_model()
    query = request.GET.get('q', '')
    users = User.objects.all().order_by('-date_joined')
    
    if query:
        _log_with_request(
            request, logging.INFO,
            f"User list search query: '{query}' by staff user {request.user.username}"
        )
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(job_number__icontains=query) |
            Q(mobile_number__icontains=query)
        )
    
    context = {
        'users': users,
        'query': query
    }
    return render(request, 'core/user_list.html', context)

@user_passes_test(lambda u: u.is_staff)
def user_create_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            _log_with_request(
                request, logging.INFO,
                f"Staff user {request.user.username} created new user: {user.username} ({user.job_number})"
            )
            
            # Log action
            UserActionLog.objects.create(
                user=request.user,
                action=UserActionLog.ActionType.EXPORT, # Using EXPORT as generic admin action for now or define new type
                target_object=f"Created User: {user.username}",
                details=f"Created user {user.username} ({user.job_number})",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return redirect('user_list')
    else:
        form = UserForm()
    
    return render(request, 'core/user_form.html', {'form': form, 'title': 'إضافة مستخدم جديد'})

@user_passes_test(lambda u: u.is_staff)
def user_edit_view(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    
    return render(request, 'core/user_form.html', {'form': form, 'title': f'تعديل المستخدم: {user.username}'})

@csrf_exempt
def qr_login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_string = data.get('qr_data', '')
            
            # Expected format: USER:username|JOB:job|UID:id
            parts = {}
            for part in qr_string.split('|'):
                if ':' in part:
                    key, val = part.split(':', 1)
                    parts[key] = val
            
            username = parts.get('USER')
            if not username:
                _log_with_request(
                    request, logging.WARNING,
                    f"QR login attempt with invalid format from IP {request.META.get('REMOTE_ADDR')}"
                )
                return JsonResponse({'success': False, 'message': 'تنسيق QR غير صالح'})

            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                
                # Direct login via QR (Authentication Bypass for Demo/Physical Security Context)
                # Ensure the backend actually specifies the backend to avoid errors
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                _log_with_request(
                    request, logging.INFO,
                    f"User {username} logged in via QR code from IP {request.META.get('REMOTE_ADDR')}"
                )
                
                # Log the action
                UserActionLog.objects.create(
                    user=user,
                    action=UserActionLog.ActionType.LOGIN,
                    target_object="QR Login",
                    details="تم تسجيل الدخول باستخدام بطاقة الهوية (QR)",
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                return JsonResponse({'success': True, 'redirect_url': '/intel/dashboard/'})
            except User.DoesNotExist:
                _log_with_request(
                    request, logging.WARNING,
                    f"QR login attempt for non-existent user: {username}"
                )
                return JsonResponse({'success': False, 'message': 'المستخدم غير موجود'})
        except Exception as e:
            _log_with_request(
                request, logging.ERROR,
                f"QR login exception: {str(e)}"
            )
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

def password_reset_request_view(request):
    if request.method == 'POST':
        job_number = request.POST.get('job_number')
        national_id = request.POST.get('national_id')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        
        User = get_user_model()
        
        try:
            user = User.objects.get(job_number=job_number, national_id=national_id, email=email)
            
            if new_password:
                user.set_password(new_password)
                user.save()
                
                # Log action
                UserActionLog.objects.create(
                    user=user,
                    action=UserActionLog.ActionType.OTHER,
                    target_object="Password Reset",
                    details="User successfully reset password via self-service recovery.",
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                messages.success(request, "تم تغيير كلمة المرور بنجاح. يمكنك الآن تسجيل الدخول.")
                return render(request, 'core/password_reset_recovery.html', {'success': "تم تغيير كلمة المرور بنجاح. يمكنك الآن تسجيل الدخول."})
            else:
                return render(request, 'core/password_reset_recovery.html', {'error': "يرجى إدخال كلمة المرور الجديدة."})
                
        except User.DoesNotExist:
            # Log failed attempt (generic user if possible, or just skip)
            return render(request, 'core/password_reset_recovery.html', {'error': "البيانات المدخلة غير صحيحة أو غير متطابقة."})
            
    return render(request, 'core/password_reset_recovery.html')


def health_check(request):
    """
    Health check endpoint for Railway monitoring.
    Returns JSON with status and basic system info.
    """
    from django.db import connection
    from django.conf import settings
    
    status = "healthy"
    details = {}
    
    # Check database
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        details["database"] = "connected"
    except Exception as e:
        status = "unhealthy"
        details["database"] = f"error: {str(e)}"
    
    # Check GROQ API
    if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
        details["ai_features"] = "enabled"
    else:
        details["ai_features"] = "disabled (API key missing)"
    
    response_data = {
        "status": status,
        "timestamp": "2026-01-01T00:00:00Z",  # Placeholder, use timezone.now() in real
        "details": details
    }
    
    return JsonResponse(response_data, status=200 if status == "healthy" else 503)
