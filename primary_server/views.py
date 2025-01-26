from django.shortcuts import render, redirect, get_object_or_404
from .models import Flight, Booking, AircraftData, ServerStatus
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AircraftDataSerializer
import json
from django.http import JsonResponse
from .utils import sync_to_backup_server  # Ensure this import is included

@login_required
def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)

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
    query = request.GET.get('q')
    if query:
        flights = Flight.objects.filter(departure_location__icontains=query) | Flight.objects.filter(arrival_location__icontains=query)
    else:
        flights = Flight.objects.all()
    return render(request, 'aircraft_data/flight_list.html', {'flights': flights})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'aircraft_data/booking_confirmation.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
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