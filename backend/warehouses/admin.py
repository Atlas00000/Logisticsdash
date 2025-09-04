from django.contrib import admin
from .models import WarehouseZone, WarehouseLocation, WarehouseStaff


@admin.register(WarehouseZone)
class WarehouseZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['is_active']


@admin.register(WarehouseLocation)
class WarehouseLocationAdmin(admin.ModelAdmin):
    list_display = ['location_code', 'warehouse', 'zone', 'location_type', 'capacity', 'is_active']
    list_filter = ['warehouse', 'zone', 'location_type', 'is_active']
    search_fields = ['location_code', 'warehouse__name', 'zone__name']
    list_editable = ['is_active']


@admin.register(WarehouseStaff)
class WarehouseStaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'warehouse', 'role', 'is_active', 'created_at']
    list_filter = ['warehouse', 'role', 'is_active', 'created_at']
    search_fields = ['user__username', 'warehouse__name', 'role']
    list_editable = ['is_active']
