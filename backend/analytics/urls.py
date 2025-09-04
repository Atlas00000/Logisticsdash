from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'analytics'

router = DefaultRouter()
router.register(r'dashboard-widgets', views.DashboardWidgetViewSet)
router.register(r'user-dashboards', views.UserDashboardViewSet)
router.register(r'kpi-metrics', views.KPIMetricViewSet)
router.register(r'metric-values', views.MetricValueViewSet)
router.register(r'report-templates', views.ReportTemplateViewSet)
router.register(r'scheduled-reports', views.ScheduledReportViewSet)
router.register(r'data-exports', views.DataExportViewSet)
router.register(r'analytics', views.AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]
