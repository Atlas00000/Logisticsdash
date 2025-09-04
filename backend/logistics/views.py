from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Vehicle, Driver, Route, RouteStop
from .serializers import VehicleSerializer, DriverSerializer, RouteSerializer, RouteStopSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.select_related('home_warehouse')
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vehicle_type', 'current_status', 'home_warehouse', 'is_active']
    search_fields = ['vehicle_number', 'license_plate', 'home_warehouse__name']
    ordering_fields = ['vehicle_number', 'capacity', 'fuel_efficiency', 'created_at']


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.select_related('user')
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'city', 'state', 'is_active']
    search_fields = ['user__username', 'driver_license', 'city', 'state']
    ordering_fields = ['user__username', 'experience_years', 'created_at']


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related('vehicle', 'driver', 'start_warehouse', 'end_warehouse')
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'vehicle', 'driver', 'start_warehouse', 'end_warehouse']
    search_fields = ['route_number', 'vehicle__vehicle_number', 'driver__user__username']
    ordering_fields = ['created_at', 'planned_start_time', 'total_distance']


class RouteStopViewSet(viewsets.ModelViewSet):
    queryset = RouteStop.objects.select_related('route', 'order')
    serializer_class = RouteStopSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'route', 'order']
    search_fields = ['route__route_number', 'order__order_number']
    ordering_fields = ['sequence', 'estimated_arrival', 'actual_arrival']
