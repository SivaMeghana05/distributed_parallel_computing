from django.http import JsonResponse
from .models import FlightTrack

def get_flight_positions(request):
    """API endpoint to get current positions of all active flights"""
    active_flights = FlightTrack.objects.filter(arrival_time__isnull=True)
    positions = {}
    
    for flight in active_flights:
        positions[flight.flight_number] = {
            'flight_number': flight.flight_number,
            'aircraft': flight.aircraft.model,
            'from': flight.departure_location,
            'to': flight.arrival_location,
            'latitude': flight.current_latitude or 0,
            'longitude': flight.current_longitude or 0,
            'altitude': flight.current_altitude or 30000,
        }
    
    return JsonResponse(positions) 