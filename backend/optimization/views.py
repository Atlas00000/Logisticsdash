from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from django.core.cache import cache
from django.db import connection
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
import time
from .models import (
    PerformanceMetric, SecurityEvent, CachePerformance, DatabasePerformance,
    RateLimitLog, SystemHealth, OptimizationRecommendation
)
from .serializers import (
    PerformanceMetricSerializer, SecurityEventSerializer, CachePerformanceSerializer,
    DatabasePerformanceSerializer, RateLimitLogSerializer, SystemHealthSerializer,
    OptimizationRecommendationSerializer
)


class PerformanceMetricViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['metric_type', 'endpoint']
    search_fields = ['endpoint', 'metadata']
    ordering_fields = ['timestamp', 'value', 'metric_type']


class SecurityEventViewSet(viewsets.ModelViewSet):
    queryset = SecurityEvent.objects.select_related('user')
    serializer_class = SecurityEventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event_type', 'severity', 'user']
    search_fields = ['description', 'endpoint', 'ip_address']
    ordering_fields = ['timestamp', 'severity', 'event_type']


class CachePerformanceViewSet(viewsets.ModelViewSet):
    queryset = CachePerformance.objects.all()
    serializer_class = CachePerformanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cache_type']
    search_fields = ['cache_type']
    ordering_fields = ['timestamp', 'hit_rate', 'average_response_time']


class DatabasePerformanceViewSet(viewsets.ModelViewSet):
    queryset = DatabasePerformance.objects.all()
    serializer_class = DatabasePerformanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['query_type', 'slow_query', 'table_name']
    search_fields = ['table_name', 'query_hash']
    ordering_fields = ['timestamp', 'execution_time', 'rows_affected']


class RateLimitLogViewSet(viewsets.ModelViewSet):
    queryset = RateLimitLog.objects.select_related('user')
    serializer_class = RateLimitLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['limit_type', 'blocked', 'user']
    search_fields = ['endpoint', 'ip_address']
    ordering_fields = ['timestamp', 'request_count', 'limit_threshold']


class SystemHealthViewSet(viewsets.ModelViewSet):
    queryset = SystemHealth.objects.all()
    serializer_class = SystemHealthSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['component', 'status']
    search_fields = ['component', 'error_message']
    ordering_fields = ['last_check', 'status', 'component']


class OptimizationRecommendationViewSet(viewsets.ModelViewSet):
    queryset = OptimizationRecommendation.objects.select_related('created_by', 'implemented_by')
    serializer_class = OptimizationRecommendationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['recommendation_type', 'priority', 'is_implemented']
    search_fields = ['title', 'description', 'impact']
    ordering_fields = ['priority', 'created_at', 'recommendation_type']


class SystemMonitoringViewSet(viewsets.ViewSet):
    """System monitoring and health check endpoints"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='health-check')
    def health_check(self, request):
        """Comprehensive system health check"""
        try:
            health_status = {
                'timestamp': timezone.now().isoformat(),
                'overall_status': 'HEALTHY',
                'components': {}
            }
            
            # Database health check
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    db_status = 'HEALTHY'
                    db_response_time = 0
            except Exception as e:
                db_status = 'CRITICAL'
                db_response_time = None
                health_status['overall_status'] = 'CRITICAL'
            
            health_status['components']['database'] = {
                'status': db_status,
                'response_time': db_response_time,
                'last_check': timezone.now().isoformat()
            }
            
            # Redis health check
            try:
                cache.set('health_check', 'ok', 10)
                cache_result = cache.get('health_check')
                redis_status = 'HEALTHY' if cache_result == 'ok' else 'WARNING'
            except Exception:
                redis_status = 'CRITICAL'
                health_status['overall_status'] = 'CRITICAL'
            
            health_status['components']['redis'] = {
                'status': redis_status,
                'last_check': timezone.now().isoformat()
            }
            
            # System resources
            if PSUTIL_AVAILABLE:
                try:
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    system_status = 'HEALTHY'
                    if cpu_percent > 80 or memory.percent > 80 or disk.percent > 90:
                        system_status = 'WARNING'
                    if cpu_percent > 95 or memory.percent > 95 or disk.percent > 95:
                        system_status = 'CRITICAL'
                        health_status['overall_status'] = 'CRITICAL'
                    
                    health_status['components']['system'] = {
                        'status': system_status,
                        'cpu_usage': cpu_percent,
                        'memory_usage': memory.percent,
                        'disk_usage': disk.percent,
                        'last_check': timezone.now().isoformat()
                    }
                except Exception:
                    health_status['components']['system'] = {
                        'status': 'WARNING',
                        'last_check': timezone.now().isoformat()
                    }
            else:
                health_status['components']['system'] = {
                    'status': 'WARNING',
                    'message': 'psutil not available for system monitoring',
                    'last_check': timezone.now().isoformat()
                }
            
            return Response(health_status)
            
        except Exception as e:
            return Response(
                {'error': f'Health check failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='performance-summary')
    def performance_summary(self, request):
        """Get performance metrics summary"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 7))
            end_date = timezone.now()
            start_date = end_date - timezone.timedelta(days=days)
            
            # Performance metrics summary
            response_time_avg = PerformanceMetric.objects.filter(
                metric_type='RESPONSE_TIME',
                timestamp__gte=start_date
            ).aggregate(avg_time=Avg('value'))['avg_time'] or 0
            
            error_rate = PerformanceMetric.objects.filter(
                metric_type='ERROR_RATE',
                timestamp__gte=start_date
            ).aggregate(avg_rate=Avg('value'))['avg_rate'] or 0
            
            # Cache performance summary
            cache_performance = CachePerformance.objects.filter(
                timestamp__gte=start_date
            ).aggregate(
                avg_hit_rate=Avg('hit_rate'),
                avg_response_time=Avg('average_response_time')
            )
            
            # Database performance summary
            db_performance = DatabasePerformance.objects.filter(
                timestamp__gte=start_date
            ).aggregate(
                avg_execution_time=Avg('execution_time'),
                slow_query_count=Count('id', filter=Q(slow_query=True))
            )
            
            summary = {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                },
                'performance': {
                    'average_response_time': float(response_time_avg),
                    'error_rate': float(error_rate)
                },
                'cache': {
                    'average_hit_rate': float(cache_performance['avg_hit_rate'] or 0),
                    'average_response_time': float(cache_performance['avg_response_time'] or 0)
                },
                'database': {
                    'average_execution_time': float(db_performance['avg_execution_time'] or 0),
                    'slow_query_count': db_performance['slow_query_count']
                }
            }
            
            return Response(summary)
            
        except Exception as e:
            return Response(
                {'error': f'Performance summary failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='security-summary')
    def security_summary(self, request):
        """Get security events summary"""
        try:
            # Get date range from query params
            days = int(request.query_params.get('days', 7))
            end_date = timezone.now()
            start_date = end_date - timezone.timedelta(days=days)
            
            # Security events summary
            events_by_type = SecurityEvent.objects.filter(
                timestamp__gte=start_date
            ).values('event_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            events_by_severity = SecurityEvent.objects.filter(
                timestamp__gte=start_date
            ).values('severity').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Recent critical events
            recent_critical = SecurityEvent.objects.filter(
                severity='CRITICAL',
                timestamp__gte=start_date
            ).order_by('-timestamp')[:5]
            
            summary = {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                },
                'events_by_type': list(events_by_type),
                'events_by_severity': list(events_by_severity),
                'recent_critical_events': SecurityEventSerializer(recent_critical, many=True).data
            }
            
            return Response(summary)
            
        except Exception as e:
            return Response(
                {'error': f'Security summary failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
