from django.http import JsonResponse
from .models import Flight

def active_flights_api(request):
    flights = Flight.objects.filter(status='active').values(
        'id',
        'flight_number',
        'origin',
        'destination',
        'current_lat',
        'current_lon',
        'origin_lat',
        'origin_lon',
        'destination_lat',
        'destination_lon'
    )
    return JsonResponse(list(flights), safe=False) 