from django.contrib import admin
from .models import Vehicle, Driver, Route, RouteStop


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'vehicle_type', 'license_plate', 'current_status', 'home_warehouse', 'is_active']
    list_filter = ['vehicle_type', 'current_status', 'home_warehouse', 'is_active']
    search_fields = ['vehicle_number', 'license_plate', 'home_warehouse__name']
    list_editable = ['current_status', 'is_active']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['user', 'driver_license', 'status', 'city', 'state', 'experience_years', 'is_active']
    list_filter = ['status', 'city', 'state', 'is_active']
    search_fields = ['user__username', 'driver_license', 'city']
    list_editable = ['status', 'is_active']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_number', 'vehicle', 'driver', 'start_warehouse', 'end_warehouse', 'status', 'total_distance']
    list_filter = ['status', 'vehicle', 'driver', 'start_warehouse', 'end_warehouse']
    search_fields = ['route_number', 'vehicle__vehicle_number', 'driver__user__username']
    list_editable = ['status']
    readonly_fields = ['created_at']


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['route', 'order', 'sequence', 'status', 'estimated_arrival', 'actual_arrival']
    list_filter = ['status', 'route', 'sequence']
    search_fields = ['route__route_number', 'order__order_number']
    list_editable = ['status', 'sequence']
