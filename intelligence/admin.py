from django.contrib import admin
from .models import (
    Source, IntelligenceReport, Entity, CriticalAlertRule, 
    IntelligenceNotification, SovereignTerm, IgnoredSource,
    ClassificationRule, EntityExtractionPattern, SearchConstraint
)

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_type', 'category', 'reliability_score', 'is_active', 'last_fetched_at')
    list_filter = ('source_type', 'is_active', 'category')
    search_fields = ('name', 'url')

@admin.register(IntelligenceReport)
class IntelligenceReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_at', 'classification', 'credibility_score', 'severity', 'processing_status')
    list_filter = ('classification', 'severity', 'topic', 'processing_status', 'source__source_type')
    search_fields = ('title', 'content', 'translated_title')
    date_hierarchy = 'published_at'


@admin.register(SearchConstraint)
class SearchConstraintAdmin(admin.ModelAdmin):
    list_display = ('term', 'constraint_type', 'is_active', 'created_at')
    list_filter = ('constraint_type', 'is_active')
    search_fields = ('term',)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type')
    list_filter = ('entity_type',)
    search_fields = ('name',)

@admin.register(CriticalAlertRule)
class CriticalAlertRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity_level', 'user', 'is_active')
    list_filter = ('severity_level', 'is_active')

@admin.register(SovereignTerm)
class SovereignTermAdmin(admin.ModelAdmin):
    list_display = ('english_term', 'arabic_translation', 'category', 'is_regex')
    list_filter = ('category', 'is_regex')
    search_fields = ('english_term', 'arabic_translation')

@admin.register(IgnoredSource)
class IgnoredSourceAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'reason', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('keyword',)

@admin.register(ClassificationRule)
class ClassificationRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification', 'severity', 'weight', 'is_active')
    list_filter = ('classification', 'severity', 'is_active')
    search_fields = ('name', 'keywords')

@admin.register(EntityExtractionPattern)
class EntityExtractionPatternAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'entity_type')
    list_filter = ('entity_type',)
    search_fields = ('pattern',)
