from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Invoice, InvoiceItem, Payment, PurchaseOrder, PurchaseOrderItem, Expense, FinancialReport
from .serializers import (
    InvoiceSerializer, InvoiceItemSerializer, PaymentSerializer,
    PurchaseOrderSerializer, PurchaseOrderItemSerializer, ExpenseSerializer, FinancialReportSerializer
)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('customer', 'order', 'created_by').prefetch_related('items')
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'customer', 'invoice_date']
    search_fields = ['invoice_number', 'customer__name', 'order__order_number']
    ordering_fields = ['invoice_date', 'due_date', 'total_amount']


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.select_related('invoice', 'product')
    serializer_class = InvoiceItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['invoice', 'product']
    search_fields = ['product__name']
    ordering_fields = ['quantity', 'unit_price', 'total_price']


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice', 'created_by')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'invoice']
    search_fields = ['reference_number', 'invoice__invoice_number']
    ordering_fields = ['payment_date', 'amount']


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.select_related('supplier', 'created_by').prefetch_related('items')
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'supplier', 'order_date']
    search_fields = ['po_number', 'supplier__name']
    ordering_fields = ['order_date', 'expected_delivery', 'total_amount']


class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderItem.objects.select_related('purchase_order', 'product')
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['purchase_order', 'product']
    search_fields = ['product__name']
    ordering_fields = ['quantity', 'unit_cost', 'total_cost']


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('created_by', 'approved_by')
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'expense_date']
    search_fields = ['description', 'vendor', 'receipt_reference']
    ordering_fields = ['expense_date', 'amount']


class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.select_related('created_by')
    serializer_class = FinancialReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['report_type', 'report_date']
    search_fields = ['report_type', 'summary']
    ordering_fields = ['report_date', 'period_start', 'period_end']
