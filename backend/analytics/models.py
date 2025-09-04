from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import datetime, timedelta


class DashboardWidget(models.Model):
    """Configurable dashboard widgets for users"""
    WIDGET_TYPES = [
        ('CHART', 'Chart'),
        ('METRIC', 'Metric'),
        ('TABLE', 'Table'),
        ('KPI', 'KPI Card'),
        ('TIMELINE', 'Timeline'),
    ]
    
    WIDGET_CATEGORIES = [
        ('INVENTORY', 'Inventory'),
        ('ORDERS', 'Orders'),
        ('FINANCE', 'Finance'),
        ('LOGISTICS', 'Logistics'),
        ('PERFORMANCE', 'Performance'),
        ('GENERAL', 'General'),
    ]
    
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    category = models.CharField(max_length=20, choices=WIDGET_CATEGORIES)
    description = models.TextField(blank=True)
    configuration = models.JSONField(help_text="Widget configuration and settings")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.widget_type})"


class UserDashboard(models.Model):
    """User-specific dashboard configurations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE)
    position_x = models.IntegerField(default=0, help_text="X coordinate on dashboard")
    position_y = models.IntegerField(default=0, help_text="Y coordinate on dashboard")
    width = models.IntegerField(default=4, help_text="Widget width (1-12 grid)")
    height = models.IntegerField(default=3, help_text="Widget height in rows")
    is_visible = models.BooleanField(default=True)
    custom_settings = models.JSONField(blank=True, help_text="User-specific widget settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'widget']
        ordering = ['position_y', 'position_x']

    def __str__(self):
        return f"{self.user.username} - {self.widget.name}"


class KPIMetric(models.Model):
    """Key Performance Indicators and metrics"""
    METRIC_TYPES = [
        ('COUNT', 'Count'),
        ('PERCENTAGE', 'Percentage'),
        ('CURRENCY', 'Currency'),
        ('DURATION', 'Duration'),
        ('RATIO', 'Ratio'),
    ]
    
    METRIC_CATEGORIES = [
        ('INVENTORY', 'Inventory'),
        ('ORDERS', 'Orders'),
        ('FINANCE', 'Finance'),
        ('LOGISTICS', 'Logistics'),
        ('CUSTOMER', 'Customer'),
        ('SUPPLIER', 'Supplier'),
        ('PERFORMANCE', 'Performance'),
    ]
    
    name = models.CharField(max_length=200)
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    category = models.CharField(max_length=20, choices=METRIC_CATEGORIES)
    description = models.TextField(blank=True)
    calculation_logic = models.TextField(help_text="How the metric is calculated")
    target_value = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    warning_threshold = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    critical_threshold = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class MetricValue(models.Model):
    """Historical values for KPIs and metrics"""
    metric = models.ForeignKey(KPIMetric, on_delete=models.CASCADE, related_name='values')
    value = models.DecimalField(max_digits=15, decimal_places=4)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, help_text="Additional context for the metric value")

    class Meta:
        ordering = ['-date', '-timestamp']
        unique_together = ['metric', 'date']

    def __str__(self):
        return f"{self.metric.name}: {self.value} on {self.date}"


class ReportTemplate(models.Model):
    """Predefined report templates"""
    REPORT_TYPES = [
        ('INVENTORY', 'Inventory Report'),
        ('ORDER', 'Order Report'),
        ('FINANCIAL', 'Financial Report'),
        ('LOGISTICS', 'Logistics Report'),
        ('PERFORMANCE', 'Performance Report'),
        ('CUSTOMER', 'Customer Report'),
        ('SUPPLIER', 'Supplier Report'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    template_config = models.JSONField(help_text="Report template configuration")
    parameters = models.JSONField(blank=True, help_text="Report parameters and filters")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['report_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.report_type})"


class ScheduledReport(models.Model):
    """Automated report scheduling"""
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]
    
    name = models.CharField(max_length=200)
    report_template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    recipients = models.JSONField(help_text="List of email recipients")
    parameters = models.JSONField(blank=True, help_text="Report parameters")
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.frequency})"


class DataExport(models.Model):
    """Data export history and configuration"""
    EXPORT_FORMATS = [
        ('CSV', 'CSV'),
        ('EXCEL', 'Excel'),
        ('JSON', 'JSON'),
        ('PDF', 'PDF'),
    ]
    
    EXPORT_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    name = models.CharField(max_length=200)
    export_format = models.CharField(max_length=20, choices=EXPORT_FORMATS)
    data_source = models.CharField(max_length=100, help_text="Data source for export")
    filters = models.JSONField(blank=True, help_text="Export filters and parameters")
    status = models.CharField(max_length=20, choices=EXPORT_STATUS, default='PENDING')
    file_path = models.CharField(max_length=500, blank=True, help_text="Path to exported file")
    file_size = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.export_format}) - {self.status}"
