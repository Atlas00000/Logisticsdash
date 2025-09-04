from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment, PurchaseOrder, PurchaseOrderItem, Expense, FinancialReport


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'invoice_date', 'due_date', 'status', 'total_amount']
    list_filter = ['status', 'invoice_date', 'due_date']
    search_fields = ['invoice_number', 'customer__name', 'order__order_number']
    list_editable = ['status']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [InvoiceItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'invoice', 'payment_date', 'amount', 'payment_method', 'status']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['reference_number', 'invoice__invoice_number', 'invoice__customer__name']
    list_editable = ['status']
    readonly_fields = ['created_at']


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'order_date', 'expected_delivery', 'status', 'total_amount']
    list_filter = ['status', 'order_date', 'expected_delivery']
    search_fields = ['po_number', 'supplier__name']
    list_editable = ['status']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [PurchaseOrderItemInline]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'category', 'amount', 'expense_date', 'status', 'vendor']
    list_filter = ['category', 'status', 'expense_date']
    search_fields = ['description', 'vendor', 'receipt_reference']
    list_editable = ['status', 'category']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'report_date', 'period_start', 'period_end', 'created_by']
    list_filter = ['report_type', 'report_date']
    search_fields = ['report_type', 'summary']
    readonly_fields = ['created_at']
