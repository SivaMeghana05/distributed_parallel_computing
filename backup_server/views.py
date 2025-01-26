from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Aircraft
import json
from django.utils import timezone
from .templates import BACKUP_MONITOR_TEMPLATE

def monitor_dashboard(request):
    """Serve the monitoring dashboard"""
    return HttpResponse(BACKUP_MONITOR_TEMPLATE)

@api_view(['GET'])
def get_all_aircraft(request):
    try:
        aircraft_list = Aircraft.objects.filter(is_active=True)
        data = [{
            'aircraft_id': aircraft.aircraft_id,
            'model': aircraft.model,
            'altitude': aircraft.altitude,
            'speed': aircraft.speed,
            'latitude': aircraft.latitude,
            'longitude': aircraft.longitude,
            'last_updated': aircraft.last_updated.isoformat()
        } for aircraft in aircraft_list]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def sync_aircraft_data(request):
    try:
        data = json.loads(request.body)
        aircraft_id = data.get('aircraft_id')
        
        aircraft, created = Aircraft.objects.update_or_create(
            aircraft_id=aircraft_id,
            defaults={
                'model': data.get('model'),
                'altitude': data.get('altitude'),
                'speed': data.get('speed'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'is_active': True
            }
        )
        
        return JsonResponse({
            'message': 'Aircraft data synchronized successfully',
            'created': created
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def server_status(request):
    try:
        total_aircraft = Aircraft.objects.count()
        active_aircraft = Aircraft.objects.filter(is_active=True).count()
        
        status_data = {
            'total_aircraft': total_aircraft,
            'active_aircraft': active_aircraft,
            'server_time': timezone.now().isoformat(),
            'status': 'operational'
        }
        return JsonResponse(status_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_aircraft(request, aircraft_id):
    try:
        aircraft = Aircraft.objects.get(aircraft_id=aircraft_id)
        aircraft.is_active = False
        aircraft.save()
        return JsonResponse({'message': 'Aircraft deleted successfully'})
    except Aircraft.DoesNotExist:
        return JsonResponse({'error': 'Aircraft not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 