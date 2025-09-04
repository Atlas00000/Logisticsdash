from django.contrib import admin
from .models import Customer, Supplier, CustomerContact, SupplierContact, CustomerRating, SupplierRating


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer_type', 'email', 'status', 'credit_limit', 'created_at']
    list_filter = ['customer_type', 'status', 'country', 'created_at']
    search_fields = ['name', 'email', 'phone', 'city']
    list_editable = ['status', 'credit_limit']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier_type', 'email', 'status', 'lead_time_days', 'minimum_order']
    list_filter = ['supplier_type', 'status', 'country', 'created_at']
    search_fields = ['name', 'email', 'phone', 'city']
    list_editable = ['status', 'lead_time_days', 'minimum_order']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CustomerContact)
class CustomerContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'customer', 'contact_type', 'email', 'is_active']
    list_filter = ['contact_type', 'is_active', 'customer']
    search_fields = ['first_name', 'last_name', 'email', 'customer__name']
    list_editable = ['is_active']


@admin.register(SupplierContact)
class SupplierContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'supplier', 'contact_type', 'email', 'is_active']
    list_filter = ['contact_type', 'is_active', 'supplier']
    search_fields = ['first_name', 'last_name', 'email', 'supplier__name']
    list_editable = ['is_active']


@admin.register(CustomerRating)
class CustomerRatingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'rating', 'category', 'created_by', 'created_at']
    list_filter = ['rating', 'category', 'created_at']
    search_fields = ['customer__name', 'feedback', 'category']
    readonly_fields = ['created_at']


@admin.register(SupplierRating)
class SupplierRatingAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'rating', 'category', 'created_by', 'created_at']
    list_filter = ['rating', 'category', 'created_at']
    search_fields = ['supplier__name', 'feedback', 'category']
    readonly_fields = ['created_at']
