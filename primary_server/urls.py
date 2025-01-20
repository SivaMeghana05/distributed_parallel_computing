from django.urls import path
from .views import flight_detail, book_flight, booking_confirmation, cancel_booking

urlpatterns = [
    path('flight/<int:flight_id>/', flight_detail, name='flight_detail'),
    path('book_flight/<int:flight_id>/', book_flight, name='book_flight'),
    path('booking_confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
] 