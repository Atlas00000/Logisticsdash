from django.contrib import admin
from .models import DeliveryUpdate, DriverLocation, DeliveryAlert, DeliveryPerformance


@admin.register(DeliveryUpdate)
class DeliveryUpdateAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'update_type', 'location', 'created_at']
    list_filter = ['update_type', 'created_at']
    search_fields = ['shipment__tracking_number', 'location', 'notes']
    readonly_fields = ['created_at']


@admin.register(DriverLocation)
class DriverLocationAdmin(admin.ModelAdmin):
    list_display = ['driver', 'latitude', 'longitude', 'speed', 'timestamp']
    list_filter = ['driver', 'timestamp']
    search_fields = ['driver__user__username']
    readonly_fields = ['timestamp']


@admin.register(DeliveryAlert)
class DeliveryAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_type', 'priority', 'title', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'priority', 'is_resolved', 'created_at']
    search_fields = ['title', 'message']
    list_editable = ['priority', 'is_resolved']
    readonly_fields = ['created_at']


@admin.register(DeliveryPerformance)
class DeliveryPerformanceAdmin(admin.ModelAdmin):
    list_display = ['driver', 'date', 'total_deliveries', 'successful_deliveries', 'success_rate', 'customer_rating']
    list_filter = ['driver', 'date']
    search_fields = ['driver__user__username']
    readonly_fields = ['success_rate']
