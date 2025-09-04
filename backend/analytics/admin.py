from django.contrib import admin
from .models import (
    DashboardWidget, UserDashboard, KPIMetric, MetricValue,
    ReportTemplate, ScheduledReport, DataExport
)


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'category', 'is_active', 'created_by']
    list_filter = ['widget_type', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserDashboard)
class UserDashboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'widget', 'position_x', 'position_y', 'width', 'height', 'is_visible']
    list_filter = ['is_visible', 'widget__category', 'created_at']
    search_fields = ['user__username', 'widget__name']
    list_editable = ['position_x', 'position_y', 'width', 'height', 'is_visible']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(KPIMetric)
class KPIMetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'metric_type', 'category', 'is_active', 'target_value', 'warning_threshold', 'critical_threshold', 'created_by']
    list_filter = ['metric_type', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'target_value', 'warning_threshold', 'critical_threshold']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MetricValue)
class MetricValueAdmin(admin.ModelAdmin):
    list_display = ['metric', 'value', 'date', 'timestamp']
    list_filter = ['metric__category', 'date', 'timestamp']
    search_fields = ['metric__name']
    readonly_fields = ['timestamp']


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'is_active', 'created_by']
    list_filter = ['report_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_template', 'frequency', 'is_active', 'last_run', 'next_run']
    list_filter = ['frequency', 'is_active', 'created_at']
    search_fields = ['name', 'report_template__name']
    list_editable = ['is_active', 'frequency']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DataExport)
class DataExportAdmin(admin.ModelAdmin):
    list_display = ['name', 'export_format', 'data_source', 'status', 'file_size', 'created_by']
    list_filter = ['export_format', 'status', 'created_at']
    search_fields = ['name', 'data_source']
    list_editable = ['status']
    readonly_fields = ['created_at', 'completed_at']
