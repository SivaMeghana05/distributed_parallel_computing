from django.urls import path
from . import views

urlpatterns = [
    path('', views.aircraft_list, name='aircraft_list'),
    # ... other URL patterns ...
] 
