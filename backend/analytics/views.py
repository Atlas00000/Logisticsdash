from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    DashboardWidget, UserDashboard, KPIMetric, MetricValue,
    ReportTemplate, ScheduledReport, DataExport
)
from .serializers import (
    DashboardWidgetSerializer, UserDashboardSerializer, KPIMetricSerializer,
    MetricValueSerializer, ReportTemplateSerializer, ScheduledReportSerializer, DataExportSerializer
)


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    queryset = DashboardWidget.objects.select_related('created_by')
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['widget_type', 'category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category', 'created_at']


class UserDashboardViewSet(viewsets.ModelViewSet):
    queryset = UserDashboard.objects.select_related('user', 'widget')
    serializer_class = UserDashboardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'widget', 'is_visible']
    search_fields = ['user__username', 'widget__name']
    ordering_fields = ['position_y', 'position_x']

    def get_queryset(self):
        # Users can only see their own dashboard
        return super().get_queryset().filter(user=self.request.user)


class KPIMetricViewSet(viewsets.ModelViewSet):
    queryset = KPIMetric.objects.select_related('created_by')
    serializer_class = KPIMetricSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['metric_type', 'category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category', 'created_at']


class MetricValueViewSet(viewsets.ModelViewSet):
    queryset = MetricValue.objects.select_related('metric')
    serializer_class = MetricValueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['metric', 'date']
    search_fields = ['metric__name']
    ordering_fields = ['date', 'value', 'timestamp']


class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.select_related('created_by')
    serializer_class = ReportTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['report_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'report_type', 'created_at']


class ScheduledReportViewSet(viewsets.ModelViewSet):
    queryset = ScheduledReport.objects.select_related('report_template', 'created_by')
    serializer_class = ScheduledReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['frequency', 'is_active', 'report_template']
    search_fields = ['name', 'report_template__name']
    ordering_fields = ['name', 'frequency', 'next_run']


class DataExportViewSet(viewsets.ModelViewSet):
    queryset = DataExport.objects.select_related('created_by')
    serializer_class = DataExportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['export_format', 'status', 'data_source']
    search_fields = ['name', 'data_source']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        # Users can only see their own exports
        return super().get_queryset().filter(created_by=self.request.user)


class AnalyticsViewSet(viewsets.ViewSet):
    """Analytics and business intelligence endpoints"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='dashboard-summary')
    def dashboard_summary(self, request):
        """Get dashboard summary with key metrics"""
        try:
            # Import models for analytics
            from inventory.models import Product, Inventory
            from orders.models import Order, Customer
            from finance.models import Invoice, Payment
            from logistics.models import Vehicle, Driver
            
            # Get current date and date ranges
            today = timezone.now().date()
            last_30_days = today - timedelta(days=30)
            last_7_days = today - timedelta(days=7)
            
            # Inventory metrics
            total_products = Product.objects.count()
            low_stock_products = Inventory.objects.filter(quantity__lte=10).count()
            # Calculate inventory value using F() expressions
            from django.db.models import F
            total_inventory_value = Inventory.objects.aggregate(
                total=Sum(F('quantity') * F('product__unit_price'))
            )['total'] or 0
            
            # Order metrics
            total_orders = Order.objects.count()
            orders_last_30_days = Order.objects.filter(created_at__date__gte=last_30_days).count()
            orders_last_7_days = Order.objects.filter(created_at__date__gte=last_7_days).count()
            
            # Customer metrics
            total_customers = Customer.objects.count()
            active_customers = Customer.objects.filter(is_active=True).count()
            
            # Financial metrics
            total_invoices = Invoice.objects.count()
            total_revenue = Invoice.objects.filter(status='PAID').aggregate(
                total=Sum('total_amount')
            )['total'] or 0
            pending_payments = Invoice.objects.filter(status='SENT').aggregate(
                total=Sum('total_amount')
            )['total'] or 0
            
            # Logistics metrics
            total_vehicles = Vehicle.objects.count()
            total_drivers = Driver.objects.count()
            active_routes = Driver.objects.filter(is_active=True).count()
            
            summary = {
                'inventory': {
                    'total_products': total_products,
                    'low_stock_products': low_stock_products,
                    'total_inventory_value': float(total_inventory_value),
                },
                'orders': {
                    'total_orders': total_orders,
                    'orders_last_30_days': orders_last_30_days,
                    'orders_last_7_days': orders_last_7_days,
                },
                'customers': {
                    'total_customers': total_customers,
                    'active_customers': active_customers,
                },
                'finance': {
                    'total_invoices': total_invoices,
                    'total_revenue': float(total_revenue),
                    'pending_payments': float(pending_payments),
                },
                'logistics': {
                    'total_vehicles': total_vehicles,
                    'total_drivers': total_drivers,
                    'active_routes': active_routes,
                },
                'last_updated': timezone.now().isoformat(),
            }
            
            return Response(summary)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate dashboard summary: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='inventory-analytics')
    def inventory_analytics(self, request):
        """Get inventory analytics and trends"""
        try:
            from inventory.models import Product, Inventory, InventoryTransaction
            from django.db.models import Q
            
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Product performance
            top_products = Product.objects.annotate(
                total_quantity=Sum('inventory__quantity')
            ).order_by('-total_quantity')[:10]
            
            # Low stock alerts
            low_stock_items = Inventory.objects.filter(
                quantity__lte=10
            ).select_related('product', 'warehouse')
            
            # Recent transactions
            recent_transactions = InventoryTransaction.objects.filter(
                created_at__date__gte=start_date
            ).select_related('product', 'warehouse')[:20]
            
            analytics = {
                'top_products': [
                    {
                        'name': p.name,
                        'total_quantity': p.total_quantity or 0,
                        'category': p.category.name if p.category else 'Uncategorized'
                    } for p in top_products
                ],
                'low_stock_alerts': [
                    {
                        'product': item.product.name,
                        'warehouse': item.warehouse.name,
                        'current_quantity': item.quantity,
                        'category': item.product.category.name if item.product.category else 'Uncategorized'
                    } for item in low_stock_items
                ],
                'recent_transactions': [
                    {
                        'product': t.product.name,
                        'warehouse': t.warehouse.name,
                        'transaction_type': t.transaction_type,
                        'quantity': t.quantity,
                        'date': t.created_at.date().isoformat()
                    } for t in recent_transactions
                ],
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                }
            }
            
            return Response(analytics)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate inventory analytics: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='financial-analytics')
    def financial_analytics(self, request):
        """Get financial analytics and trends"""
        try:
            from finance.models import Invoice, Payment, Expense
            from django.db.models import Q
            
            # Get date range from query params
            days = int(request.query_params.get('days', 30))
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Revenue trends
            daily_revenue = Invoice.objects.filter(
                status='PAID',
                invoice_date__gte=start_date
            ).values('invoice_date').annotate(
                daily_total=Sum('total_amount')
            ).order_by('invoice_date')
            
            # Expense breakdown
            expense_by_category = Expense.objects.filter(
                expense_date__gte=start_date
            ).values('category').annotate(
                total_amount=Sum('amount')
            ).order_by('-total_amount')
            
            # Payment methods
            payment_methods = Payment.objects.filter(
                payment_date__gte=start_date
            ).values('payment_method').annotate(
                total_amount=Sum('amount'),
                count=Count('id')
            ).order_by('-total_amount')
            
            analytics = {
                'revenue_trends': [
                    {
                        'date': item['payment_date'].isoformat(),
                        'amount': float(item['daily_total'])
                    } for item in daily_revenue
                ],
                'expense_breakdown': [
                    {
                        'category': item['category'],
                        'total_amount': float(item['total_amount'])
                    } for item in expense_by_category
                ],
                'payment_methods': [
                    {
                        'method': item['payment_method'],
                        'total_amount': float(item['total_amount']),
                        'count': item['count']
                    } for item in payment_methods
                ],
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                }
            }
            
            return Response(analytics)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate financial analytics: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
