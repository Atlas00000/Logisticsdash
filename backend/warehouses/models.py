from django.db import models
from django.contrib.auth.models import User


class WarehouseZone(models.Model):
    """Warehouse zones for organization"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WarehouseLocation(models.Model):
    """Specific locations within warehouses"""
    LOCATION_TYPES = [
        ('SHELF', 'Shelf'),
        ('BIN', 'Bin'),
        ('PALLET', 'Pallet'),
        ('AREA', 'Area'),
    ]

    warehouse = models.ForeignKey('inventory.Warehouse', on_delete=models.CASCADE)
    zone = models.ForeignKey(WarehouseZone, on_delete=models.CASCADE)
    location_code = models.CharField(max_length=50, unique=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    capacity = models.IntegerField(help_text="Capacity in units")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['warehouse', 'zone', 'location_code']

    def __str__(self):
        return f"{self.warehouse.name} - {self.zone.name} - {self.location_code}"


class WarehouseStaff(models.Model):
    """Warehouse staff management"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    warehouse = models.ForeignKey('inventory.Warehouse', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Warehouse Staff"
        ordering = ['warehouse', 'user__username']

    def __str__(self):
        return f"{self.user.username} - {self.role} at {self.warehouse.name}"
