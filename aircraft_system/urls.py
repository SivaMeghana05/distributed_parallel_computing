from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('primary_server.urls')),  # Include primary_server URLs
    path('', include('backup_server.urls')),   # Include backup_server URLs if applicable
] 