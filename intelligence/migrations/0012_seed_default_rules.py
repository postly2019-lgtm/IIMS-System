from django.db import migrations


def seed_default_rules(apps, schema_editor):
    ClassificationRule = apps.get_model('intelligence', 'ClassificationRule')
    EntityExtractionPattern = apps.get_model('intelligence', 'EntityExtractionPattern')
    IntelligenceReport = apps.get_model('intelligence', 'IntelligenceReport')

    patterns = [
        ("واشنطن", "LOC"),
        ("الرئيس", "PER"),
        ("الأمم المتحدة", "ORG"),
    ]
    for pattern, entity_type in patterns:
        EntityExtractionPattern.objects.get_or_create(
            pattern=pattern,
            defaults={"entity_type": entity_type},
        )

    ClassificationRule.objects.get_or_create(
        name="قاعدة أمنية افتراضية: هجوم/انفجار",
        defaults={
            "keywords": "انفجار,هجوم,مقتل",
            "required_keywords": "",
            "classification": "S",
            "severity": "HIGH",
            "topic": "SECURITY",
            "weight": 100,
            "is_active": True,
        },
    )


def unseed_default_rules(apps, schema_editor):
    ClassificationRule = apps.get_model('intelligence', 'ClassificationRule')
    EntityExtractionPattern = apps.get_model('intelligence', 'EntityExtractionPattern')

    EntityExtractionPattern.objects.filter(pattern__in=["واشنطن", "الرئيس", "الأمم المتحدة"]).delete()
    ClassificationRule.objects.filter(name="قاعدة أمنية افتراضية: هجوم/انفجار").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('intelligence', '0011_intelligencereport_content_ar_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_default_rules, unseed_default_rules),
    ]
