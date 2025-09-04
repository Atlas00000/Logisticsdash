from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'logistics'

router = DefaultRouter()
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'route-stops', views.RouteStopViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
