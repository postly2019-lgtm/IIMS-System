from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import UserActionLog
from .forms import UserForm
import json

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
                return JsonResponse({'success': False, 'message': 'تنسيق QR غير صالح'})

            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                
                # Direct login via QR (Authentication Bypass for Demo/Physical Security Context)
                # Ensure the backend actually specifies the backend to avoid errors
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
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
                return JsonResponse({'success': False, 'message': 'المستخدم غير موجود'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
