from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Customer, Order, OrderItem, Shipment
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer, ShipmentSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state']
    search_fields = ['name', 'email', 'city']
    ordering_fields = ['name', 'created_at']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['created_at', 'total_amount']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['order', 'product']
    search_fields = ['order__order_number', 'product__name']


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.select_related('order', 'shipped_from')
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'shipped_from']
    search_fields = ['tracking_number', 'order__order_number']
    ordering_fields = ['created_at']
