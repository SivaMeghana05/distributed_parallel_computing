from django.urls import path
from . import views

app_name = 'primary_server'

urlpatterns = [
    path('', views.home, name='home'),
    path('flights/', views.flights, name='flights'),
    path('aircraft/', views.aircraft, name='aircraft'),
    path('aircraft/<str:aircraft_id>/', views.aircraft_detail, name='aircraft_detail'),
    path('flight-data/', views.flight_data_list, name='flight_data_list'),
    path('sensor-data/', views.sensor_data_list, name='sensor_data_list'),
    path('maintenance-logs/', views.maintenance_log_list, name='maintenance_log_list'),
] 