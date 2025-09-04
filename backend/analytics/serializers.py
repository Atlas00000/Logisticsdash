from rest_framework import serializers
from .models import (
    DashboardWidget, UserDashboard, KPIMetric, MetricValue,
    ReportTemplate, ScheduledReport, DataExport
)


class DashboardWidgetSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = DashboardWidget
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserDashboardSerializer(serializers.ModelSerializer):
    widget_name = serializers.CharField(source='widget.name', read_only=True)
    widget_type = serializers.CharField(source='widget.widget_type', read_only=True)
    widget_category = serializers.CharField(source='widget.category', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserDashboard
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class KPIMetricSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = KPIMetric
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MetricValueSerializer(serializers.ModelSerializer):
    metric_name = serializers.CharField(source='metric.name', read_only=True)
    metric_category = serializers.CharField(source='metric.category', read_only=True)
    
    class Meta:
        model = MetricValue
        fields = '__all__'
        read_only_fields = ['timestamp']


class ReportTemplateSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = ReportTemplate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ScheduledReportSerializer(serializers.ModelSerializer):
    report_template_name = serializers.CharField(source='report_template.name', read_only=True)
    report_template_type = serializers.CharField(source='report_template.report_type', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = ScheduledReport
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DataExportSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = DataExport
        fields = '__all__'
        read_only_fields = ['created_at', 'completed_at']
