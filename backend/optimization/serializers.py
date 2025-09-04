from rest_framework import serializers
from .models import (
    PerformanceMetric, SecurityEvent, CachePerformance, DatabasePerformance,
    RateLimitLog, SystemHealth, OptimizationRecommendation
)


class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = '__all__'
        read_only_fields = ['timestamp']


class SecurityEventSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = SecurityEvent
        fields = '__all__'
        read_only_fields = ['timestamp']


class CachePerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CachePerformance
        fields = '__all__'
        read_only_fields = ['hit_rate', 'timestamp']


class DatabasePerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabasePerformance
        fields = '__all__'
        read_only_fields = ['timestamp']


class RateLimitLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = RateLimitLog
        fields = '__all__'
        read_only_fields = ['timestamp']


class SystemHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemHealth
        fields = '__all__'
        read_only_fields = ['last_check']


class OptimizationRecommendationSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    implemented_by_username = serializers.CharField(source='implemented_by.username', read_only=True)
    
    class Meta:
        model = OptimizationRecommendation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
