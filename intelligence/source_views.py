from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .models import Source
from core.models import UserActionLog

from .ingestion import IngestionEngine
import threading

def fetch_source_in_background(source_id):
    try:
        source = Source.objects.get(pk=source_id)
        engine = IngestionEngine()
        if source.source_type == Source.SourceType.RSS:
            engine.process_rss_source(source)
    except Exception as e:
        print(f"Background fetch failed for source {source_id}: {e}")

@login_required
@user_passes_test(lambda u: u.is_staff)
def source_manager_view(request):
    """
    View to manage sources (add, list, delete).
    Only accessible by staff/admin.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            name = request.POST.get('name')
            url = request.POST.get('url')
            category = request.POST.get('category')
            source_type = request.POST.get('source_type', Source.SourceType.WEBSITE)
            
            if name and url:
                source = Source.objects.create(
                    name=name,
                    url=url,
                    category=category,
                    source_type=source_type,
                    is_active=True
                )
                messages.success(request, f"تم إضافة المصدر: {name}")
                
                # Log action
                UserActionLog.objects.create(
                    user=request.user,
                    action=UserActionLog.ActionType.OTHER,
                    target_object=f"Source: {name}",
                    details=f"Added source URL: {url} Category: {category}",
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                # Trigger immediate fetch in background thread
                threading.Thread(target=fetch_source_in_background, args=(source.id,)).start()

            else:
                messages.error(request, "الاسم والرابط حقول مطلوبة.")
                
        elif action == 'delete':
            source_id = request.POST.get('source_id')
            source = get_object_or_404(Source, pk=source_id)
            name = source.name
            source.delete()
            messages.success(request, f"تم حذف المصدر: {name}")
            
        elif action == 'toggle':
            source_id = request.POST.get('source_id')
            source = get_object_or_404(Source, pk=source_id)
            source.is_active = not source.is_active
            source.save()
            status = "نشط" if source.is_active else "غير نشط"
            messages.success(request, f"تم تغيير حالة {source.name} إلى {status}")

        elif action == 'refresh_all':
            threading.Thread(target=IngestionEngine().fetch_all).start()
            messages.success(request, "تم بدء عملية تحديث المصادر في الخلفية.")

        return redirect('source_manager')

    # Group sources by category for display
    sources = Source.objects.all().order_by('category', 'name')
    
    # Get unique categories for filter or display
    categories = Source.objects.values_list('category', flat=True).distinct()
    
    context = {
        'sources': sources,
        'categories': categories,
        'source_types': Source.SourceType.choices
    }
    return render(request, 'intelligence/source_manager.html', context)
