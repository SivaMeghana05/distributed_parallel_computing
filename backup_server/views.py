from django.shortcuts import render
from .models import Flight

def flight_list(request):
    active_flights = Flight.objects.filter(status='active')
    inactive_flights = Flight.objects.filter(status='inactive')
    context = {
        'active_flights': active_flights,
        'inactive_flights': inactive_flights
    }
    return render(request, 'aircraft_data/flight_list.html', context) 