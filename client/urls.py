from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/aircraft-data/', views.get_aircraft_data, name='get-aircraft-data'),
] 