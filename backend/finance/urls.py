from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'finance'

router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'invoice-items', views.InvoiceItemViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'purchase-order-items', views.PurchaseOrderItemViewSet)
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'financial-reports', views.FinancialReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
