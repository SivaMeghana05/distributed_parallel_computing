from django.urls import path
from backup_app import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('aircraft/', views.flight_list, name='aircraft_list'),
] 