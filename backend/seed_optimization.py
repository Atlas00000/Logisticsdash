#!/usr/bin/env python3
"""
Seed optimization data for Week 10 testing
Creates sample performance metrics, security events, and system health data
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from optimization.models import (
    PerformanceMetric, SecurityEvent, CachePerformance, DatabasePerformance,
    RateLimitLog, SystemHealth, OptimizationRecommendation
)
from django.contrib.auth.models import User

def create_sample_optimization():
    """Create sample optimization data"""
    print("🔧 Creating sample optimization data...")
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    
    # Create performance metrics
    metric_types = ['RESPONSE_TIME', 'THROUGHPUT', 'ERROR_RATE', 'MEMORY_USAGE', 'CPU_USAGE']
    units = ['ms', 'req/s', '%', 'MB', '%']
    
    for i in range(20):
        metric_type = metric_types[i % len(metric_types)]
        unit = units[i % len(units)]
        
        if metric_type == 'RESPONSE_TIME':
            value = 50 + (i * 5)  # 50-145ms
        elif metric_type == 'THROUGHPUT':
            value = 100 + (i * 10)  # 100-290 req/s
        elif metric_type == 'ERROR_RATE':
            value = 0.1 + (i * 0.05)  # 0.1-1.05%
        elif metric_type == 'MEMORY_USAGE':
            value = 200 + (i * 15)  # 200-485 MB
        else:  # CPU_USAGE
            value = 15 + (i * 3)  # 15-72%
        
        PerformanceMetric.objects.create(
            metric_type=metric_type,
            value=value,
            unit=unit,
            endpoint=f'/api/endpoint-{i % 5}/',
            metadata={'user_id': admin_user.id, 'session_id': f'session_{i}'}
        )
    
    # Create security events
    event_types = ['LOGIN', 'LOGOUT', 'API_ACCESS', 'DATA_ACCESS', 'PERMISSION_DENIED']
    severities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    for i in range(15):
        SecurityEvent.objects.create(
            event_type=event_types[i % len(event_types)],
            severity=severities[i % len(severities)],
            user=admin_user if i % 3 == 0 else None,
            ip_address=f'192.168.1.{100 + i}',
            user_agent=f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{500 + i}',
            endpoint=f'/api/secure-endpoint-{i % 4}/',
            description=f'Security event {i + 1}: {event_types[i % len(event_types)]}',
            metadata={'browser': 'Chrome', 'os': 'Windows', 'location': 'Office'}
        )
    
    # Create cache performance data
    cache_types = ['REDIS', 'MEMORY', 'DATABASE']
    
    for i in range(10):
        cache_type = cache_types[i % len(cache_types)]
        hit_count = 1000 + (i * 100)
        miss_count = 50 + (i * 10)
        total_requests = hit_count + miss_count
        avg_response_time = 2.5 + (i * 0.3)
        
        CachePerformance.objects.create(
            cache_type=cache_type,
            hit_count=hit_count,
            miss_count=miss_count,
            total_requests=total_requests,
            average_response_time=avg_response_time
        )
    
    # Create database performance data
    query_types = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'COMPLEX']
    table_names = ['inventory', 'orders', 'customers', 'products', 'shipments']
    
    for i in range(25):
        query_type = query_types[i % len(query_types)]
        table_name = table_names[i % len(table_names)]
        execution_time = 5 + (i * 2)  # 5-53ms
        rows_affected = 1 + (i % 10)
        slow_query = execution_time > 30
        
        DatabasePerformance.objects.create(
            query_type=query_type,
            execution_time=execution_time,
            rows_affected=rows_affected,
            table_name=table_name,
            query_hash=f'hash_{i:08x}',
            slow_query=slow_query
        )
    
    # Create rate limit logs
    limit_types = ['API_RATE_LIMIT', 'USER_RATE_LIMIT', 'IP_RATE_LIMIT']
    
    for i in range(12):
        limit_type = limit_types[i % len(limit_types)]
        request_count = 50 + (i * 10)
        limit_threshold = 100
        blocked = request_count > limit_threshold
        
        RateLimitLog.objects.create(
            limit_type=limit_type,
            user=admin_user if i % 2 == 0 else None,
            ip_address=f'10.0.0.{50 + i}',
            endpoint=f'/api/rate-limited-endpoint-{i % 3}/',
            request_count=request_count,
            limit_threshold=limit_threshold,
            period_seconds=3600,
            blocked=blocked
        )
    
    # Create system health data
    components = ['DATABASE', 'REDIS', 'API', 'WORKER', 'STORAGE']
    statuses = ['HEALTHY', 'WARNING', 'HEALTHY', 'HEALTHY', 'HEALTHY']
    
    for i, (component, status) in enumerate(zip(components, statuses)):
        response_time = 5 + (i * 2) if status == 'HEALTHY' else 50 + (i * 10)
        error_message = f'Component {component} experiencing issues' if status == 'WARNING' else ''
        
        SystemHealth.objects.create(
            component=component,
            status=status,
            response_time=response_time,
            error_message=error_message,
            next_check=timezone.now() + timedelta(minutes=5),
            metadata={'component_version': '1.0', 'last_maintenance': '2024-01-01'}
        )
    
    # Create optimization recommendations
    recommendation_types = ['DATABASE', 'CACHE', 'API', 'SECURITY', 'PERFORMANCE']
    priorities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    for i in range(8):
        recommendation_type = recommendation_types[i % len(recommendation_types)]
        priority = priorities[i % len(priorities)]
        is_implemented = i % 3 == 0
        
        recommendation = OptimizationRecommendation.objects.create(
            recommendation_type=recommendation_type,
            priority=priority,
            title=f'Optimize {recommendation_type.lower()} performance',
            description=f'Detailed description for {recommendation_type} optimization {i + 1}',
            impact=f'Expected to improve {recommendation_type.lower()} performance by 20-30%',
            implementation=f'Step-by-step implementation guide for {recommendation_type} optimization',
            estimated_effort=f'{2 + i} days',
            is_implemented=is_implemented,
            implemented_at=timezone.now() if is_implemented else None,
            implemented_by=admin_user if is_implemented else None,
            created_by=admin_user
        )
    
    print("✅ Created performance metrics, security events, and optimization data")
    print(f"📊 Total records: {PerformanceMetric.objects.count()} performance metrics, {SecurityEvent.objects.count()} security events")
    print(f"⚡ Total records: {CachePerformance.objects.count()} cache performance, {DatabasePerformance.objects.count()} database performance")
    print(f"🛡️ Total records: {RateLimitLog.objects.count()} rate limit logs, {SystemHealth.objects.count()} system health")
    print(f"🔧 Total records: {OptimizationRecommendation.objects.count()} optimization recommendations")

if __name__ == "__main__":
    create_sample_optimization()
