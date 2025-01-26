from django.shortcuts import render
from aircraft_primary_server.models import Aircraft, ServerStatus
from django.db.models import Count
from django.utils import timezone

def dashboard(request):
    # Get data from primary server
    aircraft_list = Aircraft.objects.all()
    server_status = ServerStatus.objects.first()
    
    # If no server status exists, create one
    if not server_status:
        server_status = ServerStatus.objects.create(
            is_active=True,
            server_type='PRIMARY'
        )
    
    # Calculate statistics
    total_aircraft = aircraft_list.count()
    active_flights = aircraft_list.filter(
        altitude__gt=0  # Assuming aircraft with altitude > 0 are active flights
    ).count()
    
    # Prepare context data
    context = {
        'aircraft_list': aircraft_list,
        'server_status': server_status,
        'total_aircraft': total_aircraft,
        'active_flights': active_flights,
        'active_server': 'Primary' if server_status.is_active else 'Backup',
        'system_health': '100%',  # We'll make this dynamic later
        'last_updated': timezone.now(),
        'flights': aircraft_list.values(
            'aircraft_id',
            'model',
            'altitude',
            'speed',
            'latitude',
            'longitude'
        )
    }
    
    return render(request, 'aircraft_data/dashboard.html', context) 