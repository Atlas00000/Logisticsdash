from django.contrib import admin
from .models import (
    PerformanceMetric, SecurityEvent, CachePerformance, DatabasePerformance,
    RateLimitLog, SystemHealth, OptimizationRecommendation
)


@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'value', 'unit', 'endpoint', 'timestamp']
    list_filter = ['metric_type', 'unit', 'timestamp']
    search_fields = ['endpoint', 'metadata']
    readonly_fields = ['timestamp']
    list_per_page = 100


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'severity', 'user', 'ip_address', 'endpoint', 'timestamp']
    list_filter = ['event_type', 'severity', 'timestamp']
    search_fields = ['user__username', 'ip_address', 'endpoint', 'description']
    readonly_fields = ['timestamp']
    list_per_page = 100


@admin.register(CachePerformance)
class CachePerformanceAdmin(admin.ModelAdmin):
    list_display = ['cache_type', 'hit_count', 'miss_count', 'hit_rate', 'average_response_time', 'timestamp']
    list_filter = ['cache_type', 'timestamp']
    search_fields = ['cache_type']
    readonly_fields = ['hit_rate', 'timestamp']
    list_per_page = 100


@admin.register(DatabasePerformance)
class DatabasePerformanceAdmin(admin.ModelAdmin):
    list_display = ['query_type', 'execution_time', 'rows_affected', 'table_name', 'slow_query', 'timestamp']
    list_filter = ['query_type', 'slow_query', 'table_name', 'timestamp']
    search_fields = ['table_name', 'query_hash']
    readonly_fields = ['timestamp']
    list_per_page = 100


@admin.register(RateLimitLog)
class RateLimitLogAdmin(admin.ModelAdmin):
    list_display = ['limit_type', 'user', 'ip_address', 'endpoint', 'request_count', 'blocked', 'timestamp']
    list_filter = ['limit_type', 'blocked', 'timestamp']
    search_fields = ['user__username', 'ip_address', 'endpoint']
    readonly_fields = ['timestamp']
    list_per_page = 100


@admin.register(SystemHealth)
class SystemHealthAdmin(admin.ModelAdmin):
    list_display = ['component', 'status', 'response_time', 'last_check', 'next_check']
    list_filter = ['component', 'status', 'last_check']
    search_fields = ['component', 'error_message']
    list_editable = ['status', 'next_check']
    readonly_fields = ['last_check']


@admin.register(OptimizationRecommendation)
class OptimizationRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recommendation_type', 'priority', 'is_implemented', 'created_by', 'created_at']
    list_filter = ['recommendation_type', 'priority', 'is_implemented', 'created_at']
    search_fields = ['title', 'description', 'impact']
    list_editable = ['priority', 'is_implemented']
    readonly_fields = ['created_at', 'updated_at']
