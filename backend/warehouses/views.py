from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import WarehouseZone, WarehouseLocation, WarehouseStaff
from .serializers import WarehouseZoneSerializer, WarehouseLocationSerializer, WarehouseStaffSerializer


class WarehouseZoneViewSet(viewsets.ModelViewSet):
    queryset = WarehouseZone.objects.all()
    serializer_class = WarehouseZoneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class WarehouseLocationViewSet(viewsets.ModelViewSet):
    queryset = WarehouseLocation.objects.select_related('warehouse', 'zone')
    serializer_class = WarehouseLocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warehouse', 'zone', 'location_type', 'is_active']
    search_fields = ['location_code', 'warehouse__name', 'zone__name']
    ordering_fields = ['warehouse', 'zone', 'location_code']


class WarehouseStaffViewSet(viewsets.ModelViewSet):
    queryset = WarehouseStaff.objects.select_related('user', 'warehouse')
    serializer_class = WarehouseStaffSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warehouse', 'role', 'is_active']
    search_fields = ['user__username', 'warehouse__name', 'role']
    ordering_fields = ['warehouse', 'user__username', 'created_at']
