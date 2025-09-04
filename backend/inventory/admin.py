from django.contrib import admin
from .models import Category, Product, Warehouse, Inventory, InventoryTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'unit_price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['sku', 'name', 'description']
    list_editable = ['is_active']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'country', 'capacity', 'is_active']
    list_filter = ['is_active', 'country', 'state']
    search_fields = ['name', 'city', 'address']
    list_editable = ['is_active']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'reorder_level', 'last_updated']
    list_filter = ['warehouse', 'last_updated']
    search_fields = ['product__name', 'warehouse__name']
    list_editable = ['quantity', 'reorder_level']


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'transaction_type', 'quantity', 'created_by', 'created_at']
    list_filter = ['transaction_type', 'warehouse', 'created_at']
    search_fields = ['product__name', 'warehouse__name', 'reference']
    readonly_fields = ['created_at']
