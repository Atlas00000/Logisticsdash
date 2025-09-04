from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inventory'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'warehouse-info', views.WarehouseViewSet)
router.register(r'inventory', views.InventoryViewSet)
router.register(r'transactions', views.InventoryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
