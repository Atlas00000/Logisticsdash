from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request, format=None):
    """
    Comprehensive API root showing all available endpoints
    """
    return Response({
        # Inventory Management
        'categories': 'http://localhost:8000/api/categories/',
        'products': 'http://localhost:8000/api/products/',
        'warehouse-info': 'http://localhost:8000/api/warehouse-info/',
        'inventory': 'http://localhost:8000/api/inventory/',
        'transactions': 'http://localhost:8000/api/transactions/',
        
        # Order Management
        'order-customers': 'http://localhost:8000/api/order-customers/',
        'orders': 'http://localhost:8000/api/orders/',
        'order-items': 'http://localhost:8000/api/order-items/',
        'shipments': 'http://localhost:8000/api/shipments/',
        
        # Warehouse Management
        'zones': 'http://localhost:8000/api/zones/',
        'locations': 'http://localhost:8000/api/locations/',
        'staff': 'http://localhost:8000/api/staff/',
        
        # Logistics Management
        'vehicles': 'http://localhost:8000/api/vehicles/',
        'drivers': 'http://localhost:8000/api/drivers/',
        'routes': 'http://localhost:8000/api/routes/',
        
        # Tracking & Monitoring
        'delivery-updates': 'http://localhost:8000/api/delivery-updates/',
        'driver-locations': 'http://localhost:8000/api/driver-locations/',
        'delivery-alerts': 'http://localhost:8000/api/delivery-alerts/',
        
        # Partner Management
        'customers': 'http://localhost:8000/api/customers/',
        'suppliers': 'http://localhost:8000/api/suppliers/',
        'customer-contacts': 'http://localhost:8000/api/customer-contacts/',
        'supplier-contacts': 'http://localhost:8000/api/supplier-contacts/',
        'customer-ratings': 'http://localhost:8000/api/customer-ratings/',
        'supplier-ratings': 'http://localhost:8000/api/supplier-ratings/',
        
        # Financial Management
        'invoices': 'http://localhost:8000/api/invoices/',
        'payments': 'http://localhost:8000/api/payments/',
        'purchase-orders': 'http://localhost:8000/api/purchase-orders/',
        'expenses': 'http://localhost:8000/api/expenses/',
        'financial-reports': 'http://localhost:8000/api/financial-reports/',
        
        # Analytics & Dashboard
        'dashboard-widgets': 'http://localhost:8000/api/dashboard-widgets/',
        'user-dashboards': 'http://localhost:8000/api/user-dashboards/',
        'kpi-metrics': 'http://localhost:8000/api/kpi-metrics/',
        'metric-values': 'http://localhost:8000/api/metric-values/',
        'report-templates': 'http://localhost:8000/api/report-templates/',
        'scheduled-reports': 'http://localhost:8000/api/scheduled-reports/',
        'data-exports': 'http://localhost:8000/api/data-exports/',
        
        # Analytics Endpoints
        'analytics': {
            'dashboard-summary': 'http://localhost:8000/api/analytics/dashboard-summary/',
            'inventory-analytics': 'http://localhost:8000/api/analytics/inventory-analytics/',
            'financial-analytics': 'http://localhost:8000/api/analytics/financial-analytics/',
        },
        
        # Optimization & Best Practices
        'performance-metrics': 'http://localhost:8000/api/performance-metrics/',
        'security-events': 'http://localhost:8000/api/security-events/',
        'cache-performance': 'http://localhost:8000/api/cache-performance/',
        'database-performance': 'http://localhost:8000/api/database-performance/',
        'rate-limit-logs': 'http://localhost:8000/api/rate-limit-logs/',
        'system-health': 'http://localhost:8000/api/system-health/',
        'optimization-recommendations': 'http://localhost:8000/api/optimization-recommendations/',
        
        # System Monitoring
        'system-monitoring': {
            'health-check': 'http://localhost:8000/api/system-monitoring/health-check/',
            'performance-summary': 'http://localhost:8000/api/system-monitoring/performance-summary/',
            'security-summary': 'http://localhost:8000/api/system-monitoring/security-summary/',
        },
        
        # Authentication
        'auth': {
            'token': 'http://localhost:8000/api/auth/token/',
            'token-refresh': 'http://localhost:8000/api/auth/token/refresh/',
        }
    })
