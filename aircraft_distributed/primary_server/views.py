from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Aircraft
from .backup_service import backup_manager
from .templates import ADD_AIRCRAFT_TEMPLATE, MAIN_PORTAL_TEMPLATE
import json
from django.utils import timezone

def main_portal(request):
    """Serve the main portal template"""
    return HttpResponse(MAIN_PORTAL_TEMPLATE)

def add_aircraft_page(request):
    """Serve the add aircraft template"""
    return HttpResponse(ADD_AIRCRAFT_TEMPLATE)

@api_view(['GET'])
def get_all_aircraft(request):
    """Get all active aircraft"""
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
def add_aircraft(request):
    """Add new aircraft and sync to backup"""
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
        
        # Sync to backup server
        backup_manager.sync_aircraft_data({
            'aircraft_id': aircraft.aircraft_id,
            'model': aircraft.model,
            'altitude': aircraft.altitude,
            'speed': aircraft.speed,
            'latitude': aircraft.latitude,
            'longitude': aircraft.longitude
        })
        
        return JsonResponse({'message': 'Aircraft added successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_aircraft(request, aircraft_id):
    """Delete aircraft and sync deletion to backup"""
    try:
        aircraft = Aircraft.objects.get(aircraft_id=aircraft_id)
        aircraft.is_active = False
        aircraft.save()
        
        # Notify backup server
        backup_manager.notify_aircraft_deletion(aircraft_id)
        
        return JsonResponse({'message': 'Aircraft deleted successfully'})
    except Aircraft.DoesNotExist:
        return JsonResponse({'error': 'Aircraft not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def system_status(request):
    """Get system status including backup server status"""
    try:
        backup_status = backup_manager.get_backup_status()
        active_count = Aircraft.objects.filter(is_active=True).count()
        
        status_data = {
            'active_aircraft': active_count,
            'backup_server_available': backup_status['is_available'],
            'last_backup_sync': backup_status['last_sync_time'],
            'backup_errors': backup_status['sync_errors'],
            'system_time': timezone.now().isoformat()
        }
        
        return JsonResponse(status_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def health_check(request):
    """Basic health check endpoint"""
    return JsonResponse({'status': 'healthy'}) 