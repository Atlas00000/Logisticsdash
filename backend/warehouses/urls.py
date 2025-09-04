from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'warehouses'

router = DefaultRouter()
router.register(r'zones', views.WarehouseZoneViewSet)
router.register(r'locations', views.WarehouseLocationViewSet)
router.register(r'staff', views.WarehouseStaffViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
