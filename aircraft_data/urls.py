from django.urls import path
from . import views

app_name = 'aircraft_data'

urlpatterns = [
    path('', views.aircraft_list, name='aircraft_list'),
    path('aircraft/<int:pk>/', views.aircraft_detail, name='aircraft_detail'),
    path('maintenance/', views.maintenance_dashboard, name='maintenance_dashboard'),
    path('flights/inactive/', views.inactive_flights, name='inactive_flights'),
    path('api/flight-positions/', views.flight_positions, name='flight_positions'),
]


