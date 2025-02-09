from django.shortcuts import render
from django.http import JsonResponse
from .models import Aircraft, ServerStatus
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_aircraft(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aircraft = Aircraft.objects.create(
                aircraft_id=data['aircraft_id'],
                model=data['model'],
                altitude=data['altitude'],
                speed=data['speed'],
                latitude=data['latitude'],
                longitude=data['longitude']
            )
            return JsonResponse({'status': 'success', 'message': 'Aircraft added successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def get_aircraft_list(request):
    aircraft_list = Aircraft.objects.all().values()
    return JsonResponse({'aircraft': list(aircraft_list)})

def get_server_status(request):
    status = ServerStatus.objects.first()
    if not status:
        status = ServerStatus.objects.create()
    return JsonResponse({
        'is_active': status.is_active,
        'last_heartbeat': status.last_heartbeat.isoformat(),
        'server_type': status.server_type
    }) 