from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin endpoint
    path('admin/', admin.site.urls),
    # Include all API URLs with /api prefix
    path('api/', include('server.api_urls')),
]