from rest_framework import serializers
from .models import WarehouseZone, WarehouseLocation, WarehouseStaff


class WarehouseZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseZone
        fields = '__all__'


class WarehouseLocationSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    
    class Meta:
        model = WarehouseLocation
        fields = '__all__'


class WarehouseStaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    
    class Meta:
        model = WarehouseStaff
        fields = '__all__'
        read_only_fields = ['created_at']
