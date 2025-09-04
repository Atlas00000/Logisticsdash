from rest_framework import serializers
from .models import DeliveryUpdate, DriverLocation, DeliveryAlert, DeliveryPerformance


class DeliveryUpdateSerializer(serializers.ModelSerializer):
    tracking_number = serializers.CharField(source='shipment.tracking_number', read_only=True)
    route_number = serializers.CharField(source='route.route_number', read_only=True)
    
    class Meta:
        model = DeliveryUpdate
        fields = '__all__'
        read_only_fields = ['created_at']


class DriverLocationSerializer(serializers.ModelSerializer):
    driver_username = serializers.CharField(source='driver.user.username', read_only=True)
    route_number = serializers.CharField(source='route.route_number', read_only=True)
    
    class Meta:
        model = DriverLocation
        fields = '__all__'
        read_only_fields = ['timestamp']


class DeliveryAlertSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    resolved_by_username = serializers.CharField(source='resolved_by.username', read_only=True)
    
    class Meta:
        model = DeliveryAlert
        fields = '__all__'
        read_only_fields = ['created_at']


class DeliveryPerformanceSerializer(serializers.ModelSerializer):
    driver_username = serializers.CharField(source='driver.user.username', read_only=True)
    success_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = DeliveryPerformance
        fields = '__all__'
