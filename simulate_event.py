import os
import django
import random
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from intelligence.models import IntelligenceReport, Source
from django.utils import timezone

def create_simulation():
    print("🚀 Simulating Incoming Intelligence Stream...")
    
    # Ensure source
    source, _ = Source.objects.get_or_create(name="Reuters Wire (Simulated)")
    
    # Scenarios
    scenarios = [
        {
            "title": "URGENT: Cyber Attack on National Grid Infrastructure Detected",
            "content": "Intelligence intercepts indicate a coordinated cyber attack targeting the main power grid control systems. The attack vector appears to be state-sponsored. Immediate defensive countermeasures required. Severity is expected to be CRITICAL.",
            "is_critical": True
        },
        {
            "title": "Diplomatic Summit Scheduled for Next Month",
            "content": "Sources confirm that the regional diplomatic summit will proceed as planned in Riyadh next month. Agenda includes trade agreements and border security discussions.",
            "is_critical": False
        },
        {
            "title": "Suspicious Troop Movements Near Northern Border",
            "content": "Satellite imagery shows increased mobilization of mechanized infantry units 20km from the northern border. Intentions unclear but readiness state is elevated.",
            "is_critical": True
        }
    ]
    
    scenario = random.choice(scenarios)
    
    print(f"📝 Injecting Report: {scenario['title']}")
    
    report = IntelligenceReport.objects.create(
        title=scenario['title'],
        content=scenario['content'],
        source=source,
        published_at=timezone.now(),
        processing_status='PENDING', # This triggers the signal/thread
        original_language='en'
    )
    
    print(f"✅ Report Created [ID: {report.id}]. System processing started in background...")
    print("👉 Check the Dashboard for notifications!")

if __name__ == '__main__':
    create_simulation()
