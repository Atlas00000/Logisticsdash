from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Customer, Supplier, CustomerContact, SupplierContact, CustomerRating, SupplierRating
from .serializers import (
    CustomerSerializer, SupplierSerializer, CustomerContactSerializer,
    SupplierContactSerializer, CustomerRatingSerializer, SupplierRatingSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.select_related('created_by').prefetch_related('contacts', 'ratings')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer_type', 'status', 'country']
    search_fields = ['name', 'email', 'phone', 'city', 'state']
    ordering_fields = ['name', 'created_at', 'credit_limit']


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.select_related('created_by').prefetch_related('contacts', 'ratings')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['supplier_type', 'status', 'country']
    search_fields = ['name', 'email', 'phone', 'city', 'state']
    ordering_fields = ['name', 'created_at', 'lead_time_days', 'minimum_order']


class CustomerContactViewSet(viewsets.ModelViewSet):
    queryset = CustomerContact.objects.select_related('customer')
    serializer_class = CustomerContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'contact_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'customer__name']
    ordering_fields = ['first_name', 'last_name', 'contact_type']


class SupplierContactViewSet(viewsets.ModelViewSet):
    queryset = SupplierContact.objects.select_related('supplier')
    serializer_class = SupplierContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['supplier', 'contact_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'supplier__name']
    ordering_fields = ['first_name', 'last_name', 'contact_type']


class CustomerRatingViewSet(viewsets.ModelViewSet):
    queryset = CustomerRating.objects.select_related('customer', 'created_by')
    serializer_class = CustomerRatingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'rating', 'category']
    search_fields = ['customer__name', 'feedback', 'category']
    ordering_fields = ['rating', 'created_at']


class SupplierRatingViewSet(viewsets.ModelViewSet):
    queryset = SupplierRating.objects.select_related('supplier', 'created_by')
    serializer_class = SupplierRatingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['supplier', 'rating', 'category']
    search_fields = ['supplier__name', 'feedback', 'category']
    ordering_fields = ['rating', 'created_at']
