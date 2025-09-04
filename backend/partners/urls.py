from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'partners'

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'customer-contacts', views.CustomerContactViewSet)
router.register(r'supplier-contacts', views.SupplierContactViewSet)
router.register(r'customer-ratings', views.CustomerRatingViewSet)
router.register(r'supplier-ratings', views.SupplierRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
