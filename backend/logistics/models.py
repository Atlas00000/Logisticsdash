from django.db import models
from django.contrib.auth.models import User
from orders.models import Order, Shipment
from inventory.models import Warehouse


class Vehicle(models.Model):
    """Vehicle fleet management"""
    VEHICLE_TYPES = [
        ('TRUCK', 'Delivery Truck'),
        ('VAN', 'Delivery Van'),
        ('CAR', 'Car'),
        ('MOTORCYCLE', 'Motorcycle'),
    ]
    
    VEHICLE_STATUS = [
        ('AVAILABLE', 'Available'),
        ('IN_USE', 'In Use'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('OUT_OF_SERVICE', 'Out of Service'),
    ]

    vehicle_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    license_plate = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField(help_text="Capacity in cubic feet")
    fuel_efficiency = models.DecimalField(max_digits=5, decimal_places=2, help_text="MPG")
    current_status = models.CharField(max_length=20, choices=VEHICLE_STATUS, default='AVAILABLE')
    home_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['vehicle_number']

    def __str__(self):
        return f"{self.vehicle_number} - {self.license_plate}"


class Driver(models.Model):
    """Driver profiles and management"""
    DRIVER_STATUS = [
        ('AVAILABLE', 'Available'),
        ('ON_DELIVERY', 'On Delivery'),
        ('OFF_DUTY', 'Off Duty'),
        ('SUSPENDED', 'Suspended'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_license = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=DRIVER_STATUS, default='AVAILABLE')
    experience_years = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} - {self.driver_license}"


class Route(models.Model):
    """Delivery route optimization"""
    ROUTE_STATUS = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    route_number = models.CharField(max_length=50, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='start_routes')
    end_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='end_routes')
    planned_start_time = models.DateTimeField()
    planned_end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ROUTE_STATUS, default='PLANNED')
    total_distance = models.DecimalField(max_digits=8, decimal_places=2, help_text="Distance in miles")
    estimated_fuel_cost = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Route {self.route_number} - {self.vehicle.vehicle_number}"


class RouteStop(models.Model):
    """Individual stops on a delivery route"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sequence = models.IntegerField(help_text="Stop sequence number")
    estimated_arrival = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    estimated_departure = models.DateTimeField()
    actual_departure = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('SKIPPED', 'Skipped'),
    ], default='PENDING')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['route', 'sequence']
        unique_together = ['route', 'sequence']

    def __str__(self):
        return f"Route {self.route.route_number} - Stop {self.sequence} - {self.order.order_number}"
