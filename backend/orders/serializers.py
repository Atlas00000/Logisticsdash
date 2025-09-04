from rest_framework import serializers
from .models import Customer, Order, OrderItem, Shipment


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    warehouse_name = serializers.CharField(source='shipped_from.name', read_only=True)
    
    class Meta:
        model = Shipment
        fields = '__all__'
        read_only_fields = ['created_at']
