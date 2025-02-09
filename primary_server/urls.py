from django.urls import path
<<<<<<< HEAD
from .views import flight_list, book_flight, booking_confirmation, cancel_booking

print("Primary server URL patterns loaded")

urlpatterns = [
    path('flights/', flight_list, name='flight_list'),
    path('book_flight/<int:flight_id>/', book_flight, name='book_flight'),
    path('booking_confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
=======
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
>>>>>>> c4ec21ac5d79b78b3a800f51e8f415bbf2eac1bf
] 