from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_aircraft, name='add_aircraft'),
    path('list/', views.get_aircraft_list, name='get_aircraft_list'),
    path('status/', views.get_server_status, name='get_server_status'),
] 