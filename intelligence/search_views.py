from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import IntelligenceReport, Source, Entity
from django.utils import timezone
from datetime import timedelta
from core.models import UserActionLog
from .url_fetcher import URLFetcher

from django.http import JsonResponse
import json

def fetch_urls_view(request):
    if request.method == 'POST':
        # Check if it's a JSON request (AJAX)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json'
        
        urls_text = ""
        fetch_query = ""
        
        if is_ajax:
            try:
                data = json.loads(request.body)
                urls = data.get('urls', [])
                fetch_query = data.get('fetch_query', '').strip()
                urls_text = "\n".join(urls) # Just for compatibility with logic below
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        else:
            urls_text = request.POST.get('urls', '')
            fetch_query = request.POST.get('fetch_query', '').strip()

        if urls_text or (is_ajax and urls):
            if is_ajax:
                urls_list = urls # Already a list from JSON
            else:
                urls_list = [url.strip() for url in urls_text.splitlines() if url.strip()]
            
            if urls_list:
                fetcher = URLFetcher()
                # Pass the optional query to the fetcher
                results = fetcher.fetch_and_process_urls(urls_list, query=fetch_query)
                
                msg = f"تمت العملية: {results['success']} نجاح, {results['failed']} فشل."
                if fetch_query:
                    msg += f" (تركيز البحث: {fetch_query})"
                
                if results['errors']:
                    # Show first few errors if any
                    msg += f" أخطاء: {'; '.join(results['errors'][:2])}..."
                
                # Log action
                if request.user.is_authenticated:
                    UserActionLog.objects.create(
                        user=request.user,
                        action=UserActionLog.ActionType.INGEST,
                        target_object=f"Manual URL Fetch ({len(urls_list)} URLs)",
                        details=f"Query: {fetch_query} | Success: {results['success']}",
                        ip_address=request.META.get('REMOTE_ADDR')
                    )

                if is_ajax:
                    return JsonResponse({
                        'status': 'success', 
                        'message': msg,
                        'results': results
                    })
                
                if results['success'] > 0:
                    messages.success(request, msg)
                else:
                    messages.error(request, msg)
                
            else:
                if is_ajax:
                    return JsonResponse({'status': 'warning', 'message': "لم يتم إدخال روابط صالحة."}, status=400)
                messages.warning(request, "لم يتم إدخال روابط صالحة.")
        else:
            if is_ajax:
                return JsonResponse({'status': 'warning', 'message': "الرجاء إدخال روابط."}, status=400)
            messages.warning(request, "الرجاء إدخال روابط.")
            
    if is_ajax:
        return JsonResponse({'status': 'error', 'message': 'Invalid Method'}, status=405)
    return redirect('search')

def search_view(request):
    query = request.GET.get('q', '')
    classification = request.GET.get('classification', '')
    source_id = request.GET.get('source', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # Audit Log for Search
    if request.user.is_authenticated and query:
        UserActionLog.objects.create(
            user=request.user,
            action=UserActionLog.ActionType.SEARCH,
            target_object=f"Query: {query}",
            details=f"Filters - Class: {classification}, Source: {source_id}, Date: {date_from}-{date_to}",
            ip_address=request.META.get('REMOTE_ADDR')
        )

    reports = IntelligenceReport.objects.all().order_by('-published_at')

    if query:
        reports = reports.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(entities__name__icontains=query)
        ).distinct()

    if classification:
        reports = reports.filter(classification=classification)

    if source_id:
        reports = reports.filter(source_id=source_id)

    if date_from:
        reports = reports.filter(published_at__gte=date_from)

    if date_to:
        reports = reports.filter(published_at__lte=date_to)

    context = {
        'reports': reports,
        'query': query,
        'sources': Source.objects.filter(is_active=True),
        'classifications': IntelligenceReport.Classification.choices,
    }
    return render(request, 'intelligence/search.html', context)
