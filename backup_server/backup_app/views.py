from django.shortcuts import render
from primary_server.models import Flight

def flight_list(request):
    active_flights = Flight.objects.filter(status='active')
    context = {
        'active_flights': active_flights,
    }
    return render(request, 'aircraft_data/flight_list.html', context)
