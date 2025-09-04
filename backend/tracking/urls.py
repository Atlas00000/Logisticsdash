from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'tracking'

router = DefaultRouter()
router.register(r'delivery-updates', views.DeliveryUpdateViewSet)
router.register(r'driver-locations', views.DriverLocationViewSet)
router.register(r'delivery-alerts', views.DeliveryAlertViewSet)
router.register(r'delivery-performance', views.DeliveryPerformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
