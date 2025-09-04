from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Customer(models.Model):
    """Customer information and preferences"""
    CUSTOMER_TYPES = [
        ('INDIVIDUAL', 'Individual'),
        ('BUSINESS', 'Business'),
        ('WHOLESALE', 'Wholesale'),
        ('RETAIL', 'Retail'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    name = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='INDIVIDUAL')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Enter a valid phone number')
    ])
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_terms = models.CharField(max_length=100, default='Net 30')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.customer_type})"


class Supplier(models.Model):
    """Supplier information and capabilities"""
    SUPPLIER_TYPES = [
        ('MANUFACTURER', 'Manufacturer'),
        ('DISTRIBUTOR', 'Distributor'),
        ('WHOLESALER', 'Wholesaler'),
        ('SERVICE', 'Service Provider'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('APPROVED', 'Approved'),
        ('PENDING', 'Pending Approval'),
    ]
    
    name = models.CharField(max_length=200)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPES, default='DISTRIBUTOR')
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Enter a valid phone number')
    ])
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    tax_id = models.CharField(max_length=50, blank=True)
    payment_terms = models.CharField(max_length=100, default='Net 30')
    lead_time_days = models.IntegerField(default=7, help_text="Typical lead time in days")
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.supplier_type})"


class CustomerContact(models.Model):
    """Customer contact persons"""
    CONTACT_TYPES = [
        ('PRIMARY', 'Primary Contact'),
        ('BILLING', 'Billing Contact'),
        ('TECHNICAL', 'Technical Contact'),
        ('EMERGENCY', 'Emergency Contact'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES, default='PRIMARY')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Enter a valid phone number')
    ])
    title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['customer', 'contact_type']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.contact_type}"


class SupplierContact(models.Model):
    """Supplier contact persons"""
    CONTACT_TYPES = [
        ('PRIMARY', 'Primary Contact'),
        ('SALES', 'Sales Contact'),
        ('TECHNICAL', 'Technical Contact'),
        ('ACCOUNTS', 'Accounts Payable'),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='contacts')
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES, default='PRIMARY')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Enter a valid phone number')
    ])
    title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['supplier', 'contact_type']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.contact_type}"


class CustomerRating(models.Model):
    """Customer satisfaction ratings and feedback"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Rating from 1-5")
    feedback = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True, help_text="e.g., Delivery, Quality, Service")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.name} - {self.rating}/5"


class SupplierRating(models.Model):
    """Supplier performance ratings and feedback"""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Rating from 1-5")
    feedback = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True, help_text="e.g., Quality, Delivery, Price")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.supplier.name} - {self.rating}/5"
