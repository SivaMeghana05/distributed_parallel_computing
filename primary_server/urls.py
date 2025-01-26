from django.urls import path
from . import views

app_name = 'primary_server'

urlpatterns = [
    path('', views.main_portal, name='main_portal'),
    path('add/', views.add_aircraft_page, name='add_aircraft_page'),
    path('aircraft/', views.get_all_aircraft, name='get_all_aircraft'),
    path('add/submit/', views.add_aircraft, name='add_aircraft'),
    path('delete/<str:aircraft_id>/', views.delete_aircraft, name='delete_aircraft'),
    path('status/', views.system_status, name='system_status'),
    path('health/', views.health_check, name='health_check'),
    path('api/flight-positions/', views.flight_positions, name='flight_positions'),
] 