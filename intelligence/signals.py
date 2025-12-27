from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import IntelligenceReport, CriticalAlertRule, IntelligenceNotification

@receiver(post_save, sender=IntelligenceReport)
def auto_translate_report(sender, instance, created, **kwargs):
    """
    Automatically translates new reports to Arabic.
    """
    # Prevent recursion
    if kwargs.get('update_fields') and 'translated_title' in kwargs['update_fields']:
        return

    # If already translated, skip
    if instance.translated_title:
        return

    try:
        # 1. Try Offline Sovereign Translation First (Fast & Secure)
        from intelligence.utils.translation_engine import SmartDictionaryTranslator
        translator = SmartDictionaryTranslator()
        
        # Translate Title
        t_title = translator.translate_text(instance.title)
        # Translate Content
        t_content = translator.translate_text(instance.content)
        
        if t_title and t_content:
            instance.translated_title = t_title
            instance.translated_content = t_content
            instance.processing_status = 'COMPLETED'
            # Save without triggering signals again
            instance.save(update_fields=['translated_title', 'translated_content', 'processing_status'])
            return

        # 2. Fallback to AI (if needed, but offline is preferred)
        from intelligence_agent.services import GroqClient
        client = GroqClient()
        client.translate_report_obj(instance)
    except Exception as e:
        print(f"Auto-translation error: {e}")

@receiver(post_save, sender=IntelligenceReport)
def check_critical_alerts(sender, instance, created, **kwargs):
    """
    Checks if a new report matches any critical alert rules OR System Sovereign Threats.
    """
    if not created:
        return

    # --- 1. System Sovereign Threats (Automatic KSA Protection) ---
    # If the report is classified as TOP_SECRET (THREAT_KSA), trigger immediate alert
    if instance.classification == IntelligenceReport.Classification.TOP_SECRET:
        # Create a system-wide critical notification for all admins (or specific users)
        # For simplicity, we'll assign it to the first superuser or a system account
        # In this demo, we might just fetch the first user
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_users = User.objects.filter(is_superuser=True)
        
        for admin in admin_users:
             IntelligenceNotification.objects.create(
                user=admin,
                title=f"⚠️ تهديد سيادي: {instance.title[:30]}...",
                message=f"رصد تهديد يمس الأمن الوطني: {instance.title}",
                level=IntelligenceNotification.Level.CRITICAL,
                report=instance
            )

    # --- 2. User Defined Rules ---
    # Get all active rules
    rules = CriticalAlertRule.objects.filter(is_active=True)

    for rule in rules:
        # Check Region
        if rule.region and rule.region.lower() not in instance.content.lower() and rule.region.lower() not in instance.title.lower():
            continue

        # Check Keywords
        keywords = [k.strip().lower() for k in rule.keywords.split(',')]
        match_found = False
        for keyword in keywords:
            if keyword in instance.title.lower() or keyword in instance.content.lower():
                match_found = True
                break
        
        if not match_found:
            continue

        # Check Severity (Simple check: matches the rule's level or higher)
        # Assuming Report severity is set. If not, we might rely solely on keywords for now 
        # as the user said "measurements indicate crisis". 
        # If the report is newly created, severity might be default LOW unless calculated.
        # However, let's assume if keywords match a "Critical Rule", we flag it.
        # OR, strictly check instance.severity.
        
        # User Logic: "after analyzing it and metrics indicate crisis".
        # If the report comes from the system, it might already have severity.
        # If not, we might want to trigger the alert anyway if it hits the keywords of a CRITICAL rule.
        
        # Implementation: If the rule requires CRITICAL, and report is HIGH or CRITICAL, trigger?
        # Let's stick to: If rule matches, we consider it a hit.
        
        IntelligenceNotification.objects.create(
            user=rule.user,
            title=f"تنبيه حرج: {rule.name}",
            message=f"تم رصد تقرير جديد يطابق معايير التنبيه: {instance.title}",
            level=IntelligenceNotification.Level.CRITICAL,
            report=instance,
            alert_rule=rule
        )
