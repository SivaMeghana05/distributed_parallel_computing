from django.shortcuts import render, redirect, get_object_or_404
from .models import Flight, Booking
from django.contrib.auth.decorators import login_required

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