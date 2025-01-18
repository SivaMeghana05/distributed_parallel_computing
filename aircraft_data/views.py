from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Aircraft, FlightTrack, MaintenanceSchedule, PerformanceMetric, Flight
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.http import JsonResponse

@login_required
def home(request):
    return render(request, 'aircraft_data/home.html')

@login_required
def aircraft_list(request):
    # Get all aircraft and flights
    aircrafts = Aircraft.objects.all().order_by('-last_updated')
    flights = FlightTrack.objects.all().order_by('-departure_time')
    
    # Aircraft status counts
    status_counts = {
        'total': 23,
        'active': 11,
        'maintenance': 7,
        'inactive': 5,
    }
    
    # Flight statistics
    flight_stats = {
        'total_flights': 22,
        'total_routes': len(set([f"{flight.departure_location}-{flight.arrival_location}" for flight in flights])),
        'domestic_routes': flights.filter(
            departure_location__in=['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad']
        ).count(),
        'international_routes': flights.exclude(
            departure_location__in=['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad']
        ).count(),
    }
    
    return render(request, 'aircraft_data/dashboard.html', {
        'aircrafts': aircrafts,
        'flights': flights,
        'status_counts': status_counts,
        'flight_stats': flight_stats,
    })

@login_required
def aircraft_detail(request, pk):
    aircraft = get_object_or_404(Aircraft, pk=pk)
    flights = FlightTrack.objects.filter(aircraft=aircraft).order_by('-departure_time')
    return render(request, 'aircraft_data/aircraft_detail.html', {
        'aircraft': aircraft,
        'flights': flights
    })

@login_required
def aircraft_update(request, pk):
    aircraft = get_object_or_404(Aircraft, pk=pk)
    if request.method == 'POST':
        # Add your update logic here
        pass
    return render(request, 'aircraft_data/aircraft_form.html', {'aircraft': aircraft})

@login_required
def flight_tracking(request, flight_id):
    flight = get_object_or_404(FlightTrack, pk=flight_id)
    return render(request, 'aircraft_data/flight_tracking.html', {'flight': flight})

@login_required
def flight_list(request):
    active_flights = FlightTrack.objects.filter(arrival_time__isnull=True)
    completed_flights = FlightTrack.objects.filter(arrival_time__isnull=False)
    return render(request, 'aircraft_data/flight_list.html', {
        'active_flights': active_flights,
        'completed_flights': completed_flights
    })

@login_required
def flight_detail(request, pk):
    flight = get_object_or_404(FlightTrack, pk=pk)
    return render(request, 'aircraft_data/flight_detail.html', {
        'flight': flight
    })

@login_required
def maintenance_dashboard(request):
    maintenance_schedules = MaintenanceSchedule.objects.all().order_by('scheduled_date')
    
    # Get counts for different maintenance statuses
    status_counts = {
        'scheduled': maintenance_schedules.filter(status='scheduled').count(),
        'in_progress': maintenance_schedules.filter(status='in_progress').count(),
        'completed': maintenance_schedules.filter(status='completed').count(),
        'overdue': maintenance_schedules.filter(
            status='scheduled',
            scheduled_date__lt=timezone.now()
        ).count(),
    }
    
    # Get performance metrics
    performance_metrics = PerformanceMetric.objects.all().order_by('-date_recorded')[:10]
    
    return render(request, 'aircraft_data/maintenance_dashboard.html', {
        'maintenance_schedules': maintenance_schedules,
        'status_counts': status_counts,
        'performance_metrics': performance_metrics,
    })

class AircraftListView(ListView):
    model = Aircraft
    template_name = 'aircraft_data/aircraft_list.html'
    context_object_name = 'aircrafts'

def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('aircraft_data:aircraft_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def flight_positions(request):
    """API endpoint to get all active flight positions"""
    flights = Flight.objects.filter(status='active')
    positions = {}
    for flight in flights:
        positions[flight.id] = {
            'flight_number': flight.flight_number,
            'latitude': str(flight.current_latitude) if flight.current_latitude else '0',
            'longitude': str(flight.current_longitude) if flight.current_longitude else '0',
            'altitude': str(flight.current_altitude) if flight.current_altitude else '0',
            'from': flight.departure_location,
            'to': flight.arrival_location,
            'aircraft': flight.aircraft.model
        }
    return JsonResponse(positions)

@login_required
def inactive_flights(request):
    """View to display inactive flights"""
    inactive_flights = Flight.objects.filter(status='inactive').order_by('-departure_time')
    context = {
        'inactive_flights': inactive_flights,
        'total_inactive': inactive_flights.count(),
    }
    return render(request, 'aircraft_data/inactive_flights.html', context)