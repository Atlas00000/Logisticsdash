from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import DeliveryUpdate, DriverLocation, DeliveryAlert, DeliveryPerformance
from .serializers import (
    DeliveryUpdateSerializer, DriverLocationSerializer, 
    DeliveryAlertSerializer, DeliveryPerformanceSerializer
)


class DeliveryUpdateViewSet(viewsets.ModelViewSet):
    queryset = DeliveryUpdate.objects.select_related('shipment', 'route', 'created_by')
    serializer_class = DeliveryUpdateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['update_type', 'shipment', 'route']
    search_fields = ['shipment__tracking_number', 'location', 'notes']
    ordering_fields = ['created_at', 'update_type']


class DriverLocationViewSet(viewsets.ModelViewSet):
    queryset = DriverLocation.objects.select_related('driver', 'route')
    serializer_class = DriverLocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['driver', 'route']
    search_fields = ['driver__user__username']
    ordering_fields = ['timestamp', 'latitude', 'longitude']


class DeliveryAlertViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAlert.objects.select_related('created_by', 'resolved_by')
    serializer_class = DeliveryAlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['alert_type', 'priority', 'is_resolved']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority', 'alert_type']


class DeliveryPerformanceViewSet(viewsets.ModelViewSet):
    queryset = DeliveryPerformance.objects.select_related('driver')
    serializer_class = DeliveryPerformanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['driver', 'date']
    search_fields = ['driver__user__username']
    ordering_fields = ['date', 'total_deliveries', 'success_rate', 'customer_rating']
