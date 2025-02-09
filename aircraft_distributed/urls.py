from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('primary/', include('primary_server.urls')),
    path('backup/', include('backup_server.urls')),
]