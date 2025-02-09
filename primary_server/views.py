from django.shortcuts import render, redirect, get_object_or_404
from .models import Flight, Booking, AircraftData, ServerStatus, Aircraft, FlightData, SensorData, MaintenanceLog
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AircraftDataSerializer
import json
from django.http import JsonResponse
from django.utils import timezone
from .utils import sync_to_backup_server

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        booking = Booking(user=request.user, flight=flight, seat_number=seat_number)
        booking.save()
        return redirect('booking_confirmation', booking_id=booking.id)

    return render(request, 'aircraft_data/book_flight.html', {'flight': flight})

def flight_detail(request, flight_id):
    try:
        flight = get_object_or_404(Flight, id=flight_id)
        print(f"Flight Details: {flight}")  # Debugging line
    except Exception as e:
        print(f"Error retrieving flight: {e}")  # Print any errors

    return render(request, 'aircraft_data/flight_detail.html', {'flight': flight})

def flight_list(request):
    active_flights = Flight.objects.filter(status='active')
    inactive_flights = Flight.objects.filter(status='inactive')
    context = {
        'active_flights': active_flights,
        'inactive_flights': inactive_flights
    }
    return render(request, 'aircraft_data/flight_list.html', context)

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'aircraft_data/booking_confirmation.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
<<<<<<< HEAD
    return render(request, 'aircraft_data/cancellation_confirmation.html') 
=======
    return redirect('booking_cancellation_confirmation')  # Create a confirmation page for cancellation

class AircraftDataViewSet(viewsets.ModelViewSet):
    queryset = AircraftData.objects.all()
    serializer_class = AircraftDataSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # Trigger FTP sync to backup server
        sync_to_backup_server(instance)

@api_view(['GET'])
def server_health(request):
    try:
        status = ServerStatus.objects.get(server_type='PRIMARY')
        return Response({
            'status': 'healthy',
            'is_active': status.is_active,
            'last_heartbeat': status.last_heartbeat
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500) 

def flight_positions(request):
    print("Flight positions view called")  # Debugging line
    data = {
        "positions": [
            {"flight": "AA123", "status": "on time"},
            {"flight": "DL456", "status": "delayed"},
        ]
    }
    return JsonResponse(data)

def home(request):
    context = {
        'active_flights': Flight.objects.all(),
        'active_flights_count': Flight.objects.count(),
        'total_aircraft': Aircraft.objects.count(),
        'total_routes': 0,  # We'll add this back later
    }
    return render(request, 'primary_server/home.html', context)

def flights(request):
    context = {
        'flights': Flight.objects.all()
    }
    return render(request, 'primary_server/flights.html', context)

def aircraft(request):
    context = {
        'aircraft_list': Aircraft.objects.all()
    }
    return render(request, 'primary_server/aircraft.html', context)

def aircraft_list(request):
    aircraft = Aircraft.objects.all()
    data = [{
        'id': a.aircraft_id,
        'model': a.model,
        'manufacturer': a.manufacturer,
        'year': a.year_manufactured
    } for a in aircraft]
    return JsonResponse({'aircraft': data})

def aircraft_detail(request, aircraft_id):
    try:
        aircraft = Aircraft.objects.get(aircraft_id=aircraft_id)
        data = {
            'id': aircraft.aircraft_id,
            'model': aircraft.model,
            'manufacturer': aircraft.manufacturer,
            'year': aircraft.year_manufactured,
            'flight_count': aircraft.flightdata_set.count(),
            'sensor_count': aircraft.sensordata_set.count(),
            'maintenance_count': aircraft.maintenancelog_set.count(),
        }
        return JsonResponse(data)
    except Aircraft.DoesNotExist:
        return JsonResponse({'error': 'Aircraft not found'}, status=404)

def flight_data_list(request):
    flights = FlightData.objects.all()
    data = [{
        'flight_number': f.flight_number,
        'aircraft': f.aircraft.aircraft_id,
        'departure': f.departure_time.isoformat(),
        'arrival': f.arrival_time.isoformat() if f.arrival_time else None,
    } for f in flights]
    return JsonResponse({'flights': data})

def sensor_data_list(request):
    sensors = SensorData.objects.all()
    data = [{
        'aircraft': s.aircraft.aircraft_id,
        'type': s.sensor_type,
        'value': s.value,
        'timestamp': s.timestamp.isoformat(),
    } for s in sensors]
    return JsonResponse({'sensor_data': data})

def maintenance_log_list(request):
    logs = MaintenanceLog.objects.all()
    data = [{
        'aircraft': l.aircraft.aircraft_id,
        'type': l.maintenance_type,
        'date': l.date.isoformat(),
        'description': l.description,
    } for l in logs]
    return JsonResponse({'maintenance_logs': data})

def sync_to_backup_server(instance):
    """
    Synchronize aircraft data to backup server
    Args:
        instance: AircraftData instance to be synced
    """
    try:
        # Add your sync logic here
        # This could involve making API calls to backup server
        # or using FTP to transfer data
        pass
    except Exception as e:
        print(f"Error syncing to backup server: {e}")
        # Consider proper error handling/logging here
>>>>>>> c4ec21ac5d79b78b3a800f51e8f415bbf2eac1bf
