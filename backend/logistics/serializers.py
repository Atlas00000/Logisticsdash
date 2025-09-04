from rest_framework import serializers
from .models import Vehicle, Driver, Route, RouteStop


class VehicleSerializer(serializers.ModelSerializer):
    home_warehouse_name = serializers.CharField(source='home_warehouse.name', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['created_at']


class DriverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ['created_at']


class RouteSerializer(serializers.ModelSerializer):
    vehicle_number = serializers.CharField(source='vehicle.vehicle_number', read_only=True)
    driver_username = serializers.CharField(source='driver.user.username', read_only=True)
    start_warehouse_name = serializers.CharField(source='start_warehouse.name', read_only=True)
    end_warehouse_name = serializers.CharField(source='end_warehouse.name', read_only=True)
    
    class Meta:
        model = Route
        fields = '__all__'
        read_only_fields = ['created_at']


class RouteStopSerializer(serializers.ModelSerializer):
    route_number = serializers.CharField(source='route.route_number', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = RouteStop
        fields = '__all__'
