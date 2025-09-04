from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'optimization'

router = DefaultRouter()
router.register(r'performance-metrics', views.PerformanceMetricViewSet)
router.register(r'security-events', views.SecurityEventViewSet)
router.register(r'cache-performance', views.CachePerformanceViewSet)
router.register(r'database-performance', views.DatabasePerformanceViewSet)
router.register(r'rate-limit-logs', views.RateLimitLogViewSet)
router.register(r'system-health', views.SystemHealthViewSet)
router.register(r'optimization-recommendations', views.OptimizationRecommendationViewSet)
router.register(r'system-monitoring', views.SystemMonitoringViewSet, basename='system-monitoring')

urlpatterns = [
    path('', include(router.urls)),
]
