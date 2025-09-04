from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_root import api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', api_root, name='api-root'),
    path('api/', include('inventory.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('warehouses.urls')),
    path('api/', include('logistics.urls')),
    path('api/', include('tracking.urls')),
    path('api/', include('partners.urls')),
    path('api/', include('finance.urls')),
    path('api/', include('analytics.urls')),
    path('api/', include('optimization.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
