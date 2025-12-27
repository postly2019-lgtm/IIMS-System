import os
import django

# Updated to 'config.settings' based on LS output showing config/settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from intelligence.models import IntelligenceReport, Source
from django.db.models import Q

def clean_database():
    print("Starting database cleanup...")
    
    # 1. Delete reports from known non-intelligence domains
    ignored_keywords = [
        'nature', 'medical', 'health', 'clinic', 'science', 
        'tech', 'gadget', 'sport', 'celebrity',
        'phys.org', 'scientist', 'biology'
    ]
    
    query = Q()
    for keyword in ignored_keywords:
        query |= Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(source__name__icontains=keyword)
        
    deleted_count, _ = IntelligenceReport.objects.filter(query).delete()
    print(f"Deleted {deleted_count} non-intelligence reports.")
    
    # 2. Deactivate Sources that are purely scientific/tech
    sources = Source.objects.all()
    deactivated = 0
    for source in sources:
        name_url = (source.name + " " + (source.url or "")).lower()
        if any(k in name_url for k in ignored_keywords):
            source.is_active = False
            source.save()
            print(f"Deactivated source: {source.name}")
            deactivated += 1
            
    print(f"Deactivated {deactivated} sources.")
    print("Cleanup complete.")

if __name__ == "__main__":
    clean_database()
