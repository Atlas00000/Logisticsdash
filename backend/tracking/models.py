from django.db import models
from django.contrib.auth.models import User
from orders.models import Order, Shipment
from logistics.models import Route, Driver, Vehicle


class DeliveryUpdate(models.Model):
    """Real-time delivery status updates"""
    UPDATE_TYPES = [
        ('PICKUP', 'Order Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Delivery Failed'),
        ('RETURNED', 'Returned to Sender'),
    ]

    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True, blank=True)
    update_type = models.CharField(max_length=20, choices=UPDATE_TYPES)
    location = models.CharField(max_length=200, help_text="Current location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.update_type}"


class DriverLocation(models.Model):
    """Real-time driver location tracking"""
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Speed in MPH")
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Direction in degrees")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.driver.user.username} - {self.timestamp}"


class DeliveryAlert(models.Model):
    """Delivery alerts and notifications"""
    ALERT_TYPES = [
        ('DELAY', 'Delivery Delay'),
        ('WEATHER', 'Weather Warning'),
        ('TRAFFIC', 'Traffic Alert'),
        ('VEHICLE', 'Vehicle Issue'),
        ('DRIVER', 'Driver Issue'),
        ('CUSTOMER', 'Customer Request'),
    ]

    ALERT_PRIORITY = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    priority = models.CharField(max_length=20, choices=ALERT_PRIORITY, default='MEDIUM')
    title = models.CharField(max_length=200)
    message = models.TextField()
    affected_shipments = models.ManyToManyField(Shipment, blank=True)
    affected_routes = models.ManyToManyField(Route, blank=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_alerts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alert_type} - {self.title}"


class DeliveryPerformance(models.Model):
    """Delivery performance metrics"""
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    date = models.DateField()
    total_deliveries = models.IntegerField(default=0)
    successful_deliveries = models.IntegerField(default=0)
    failed_deliveries = models.IntegerField(default=0)
    total_distance = models.DecimalField(max_digits=8, decimal_places=2, help_text="Distance in miles")
    total_time = models.DecimalField(max_digits=6, decimal_places=2, help_text="Time in hours")
    fuel_consumed = models.DecimalField(max_digits=6, decimal_places=2, help_text="Fuel in gallons")
    customer_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, help_text="Rating out of 5")

    class Meta:
        unique_together = ['driver', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.driver.user.username} - {self.date}"

    @property
    def success_rate(self):
        if self.total_deliveries > 0:
            return (self.successful_deliveries / self.total_deliveries) * 100
        return 0
