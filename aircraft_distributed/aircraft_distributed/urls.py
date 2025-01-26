"""
URL configuration for aircraft_distributed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from aircraft_primary_server.models import Aircraft, ServerStatus

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Main dashboard
    path('admin/', admin.site.urls),
    path('primary/', include('aircraft_primary_server.urls')),
]

# Check aircraft data
print("Aircraft count:", Aircraft.objects.count())
print("\nAll aircraft:")
for aircraft in Aircraft.objects.all():
    print(f"ID: {aircraft.aircraft_id}, Model: {aircraft.model}")

# Check server status
print("\nServer Status:")
status = ServerStatus.objects.first()
if status:
    print(f"Active: {status.is_active}, Type: {status.server_type}")
