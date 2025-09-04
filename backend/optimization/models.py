from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta


class PerformanceMetric(models.Model):
    """Application performance metrics and monitoring"""
    METRIC_TYPES = [
        ('RESPONSE_TIME', 'Response Time'),
        ('THROUGHPUT', 'Throughput'),
        ('ERROR_RATE', 'Error Rate'),
        ('MEMORY_USAGE', 'Memory Usage'),
        ('CPU_USAGE', 'CPU Usage'),
        ('DATABASE_QUERIES', 'Database Queries'),
        ('CACHE_HIT_RATE', 'Cache Hit Rate'),
    ]
    
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=20, help_text="Unit of measurement")
    endpoint = models.CharField(max_length=200, blank=True, help_text="API endpoint or view")
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, help_text="Additional context")

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric_type', 'timestamp']),
            models.Index(fields=['endpoint', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.metric_type}: {self.value} {self.unit} at {self.timestamp}"


class SecurityEvent(models.Model):
    """Security events and audit logs"""
    EVENT_TYPES = [
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('AUTH_FAILURE', 'Authentication Failure'),
        ('PERMISSION_DENIED', 'Permission Denied'),
        ('API_ACCESS', 'API Access'),
        ('DATA_ACCESS', 'Data Access'),
        ('CONFIG_CHANGE', 'Configuration Change'),
        ('SECURITY_ALERT', 'Security Alert'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='LOW')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    endpoint = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    metadata = models.JSONField(blank=True, help_text="Additional event details")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['severity', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.severity} at {self.timestamp}"


class CachePerformance(models.Model):
    """Cache performance and hit rate monitoring"""
    CACHE_TYPES = [
        ('REDIS', 'Redis Cache'),
        ('MEMORY', 'Memory Cache'),
        ('DATABASE', 'Database Cache'),
        ('CDN', 'CDN Cache'),
    ]
    
    cache_type = models.CharField(max_length=20, choices=CACHE_TYPES)
    hit_count = models.BigIntegerField(default=0, help_text="Number of cache hits")
    miss_count = models.BigIntegerField(default=0, help_text="Number of cache misses")
    total_requests = models.BigIntegerField(default=0, help_text="Total cache requests")
    hit_rate = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Cache hit rate percentage"
    )
    average_response_time = models.DecimalField(
        max_digits=8, decimal_places=4, 
        help_text="Average cache response time in milliseconds"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['cache_type', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.cache_type} - {self.hit_rate}% hit rate at {self.timestamp}"

    def save(self, *args, **kwargs):
        # Auto-calculate hit rate
        if self.total_requests > 0:
            self.hit_rate = (self.hit_count / self.total_requests) * 100
        super().save(*args, **kwargs)


class DatabasePerformance(models.Model):
    """Database performance and query monitoring"""
    QUERY_TYPES = [
        ('SELECT', 'Select Query'),
        ('INSERT', 'Insert Query'),
        ('UPDATE', 'Update Query'),
        ('DELETE', 'Delete Query'),
        ('COMPLEX', 'Complex Query'),
    ]
    
    query_type = models.CharField(max_length=20, choices=QUERY_TYPES)
    execution_time = models.DecimalField(
        max_digits=8, decimal_places=4, 
        help_text="Query execution time in milliseconds"
    )
    rows_affected = models.IntegerField(default=0, help_text="Number of rows affected")
    table_name = models.CharField(max_length=100, blank=True, help_text="Main table involved")
    query_hash = models.CharField(max_length=64, blank=True, help_text="Hash of the query for identification")
    slow_query = models.BooleanField(default=False, help_text="Whether this is a slow query")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['query_type', 'timestamp']),
            models.Index(fields=['slow_query', 'timestamp']),
            models.Index(fields=['table_name', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.query_type} on {self.table_name} - {self.execution_time}ms at {self.timestamp}"


class RateLimitLog(models.Model):
    """Rate limiting and throttling logs"""
    LIMIT_TYPES = [
        ('API_RATE_LIMIT', 'API Rate Limit'),
        ('USER_RATE_LIMIT', 'User Rate Limit'),
        ('IP_RATE_LIMIT', 'IP Rate Limit'),
        ('ENDPOINT_LIMIT', 'Endpoint Limit'),
    ]
    
    limit_type = models.CharField(max_length=20, choices=LIMIT_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    endpoint = models.CharField(max_length=200)
    request_count = models.IntegerField(default=1, help_text="Number of requests in the period")
    limit_threshold = models.IntegerField(help_text="Rate limit threshold")
    period_seconds = models.IntegerField(help_text="Time period in seconds")
    blocked = models.BooleanField(default=False, help_text="Whether the request was blocked")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['limit_type', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.limit_type} - {self.ip_address} at {self.timestamp}"


class SystemHealth(models.Model):
    """System health and status monitoring"""
    COMPONENT_TYPES = [
        ('DATABASE', 'Database'),
        ('REDIS', 'Redis Cache'),
        ('API', 'API Service'),
        ('WORKER', 'Background Worker'),
        ('STORAGE', 'File Storage'),
        ('EXTERNAL_API', 'External API'),
    ]
    
    STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
        ('OFFLINE', 'Offline'),
    ]
    
    component = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_time = models.DecimalField(
        max_digits=8, decimal_places=4, 
        null=True, blank=True,
        help_text="Response time in milliseconds"
    )
    error_message = models.TextField(blank=True, help_text="Error details if any")
    last_check = models.DateTimeField(auto_now_add=True)
    next_check = models.DateTimeField(null=True, blank=True, help_text="When to check next")
    metadata = models.JSONField(blank=True, help_text="Component-specific health data")

    class Meta:
        ordering = ['component', '-last_check']
        indexes = [
            models.Index(fields=['component', 'status']),
            models.Index(fields=['status', 'last_check']),
        ]

    def __str__(self):
        return f"{self.component} - {self.status} at {self.last_check}"


class OptimizationRecommendation(models.Model):
    """System optimization recommendations"""
    RECOMMENDATION_TYPES = [
        ('DATABASE', 'Database Optimization'),
        ('CACHE', 'Cache Optimization'),
        ('API', 'API Optimization'),
        ('SECURITY', 'Security Enhancement'),
        ('PERFORMANCE', 'Performance Tuning'),
        ('SCALABILITY', 'Scalability Improvement'),
    ]
    
    PRIORITY_LEVELS = [
        ('LOW', 'Low Priority'),
        ('MEDIUM', 'Medium Priority'),
        ('HIGH', 'High Priority'),
        ('CRITICAL', 'Critical Priority'),
    ]
    
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='MEDIUM')
    title = models.CharField(max_length=200)
    description = models.TextField()
    impact = models.TextField(help_text="Expected impact of the optimization")
    implementation = models.TextField(help_text="How to implement the optimization")
    estimated_effort = models.CharField(max_length=50, help_text="Estimated effort required")
    is_implemented = models.BooleanField(default=False)
    implemented_at = models.DateTimeField(null=True, blank=True)
    implemented_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_recommendations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.priority})"
