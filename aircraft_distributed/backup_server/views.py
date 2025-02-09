from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Aircraft
from .sync_service import sync_service
import json
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

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

def monitor_dashboard(request):
    """Serve the monitoring dashboard"""
    from .templates import BACKUP_MONITOR_TEMPLATE
    return HttpResponse(BACKUP_MONITOR_TEMPLATE)

@api_view(['GET'])
def server_status(request):
    """Get detailed server status information"""
    try:
        # Get aircraft statistics
        total_aircraft = Aircraft.objects.count()
        active_aircraft = Aircraft.objects.filter(is_active=True).count()
        
        # Calculate sync success rate (last 1 hour)
        sync_status = sync_service.get_last_sync_status()
        
        # Get recent updates
        one_hour_ago = timezone.now() - timedelta(hours=1)
        recent_updates = Aircraft.objects.filter(
            last_updated__gte=one_hour_ago
        ).count()

        status_data = {
            'primary_available': sync_service.check_primary_server_health(),
            'last_sync_time': sync_status['last_sync_time'],
            'total_aircraft': total_aircraft,
            'active_aircraft': active_aircraft,
            'recent_updates': recent_updates,
            'sync_success_rate': 100 if sync_status['primary_server_available'] else 0,
        }
        
        return JsonResponse(status_data)
    except Exception as e:
        return JsonResponse(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def force_sync(request):
    """Manually trigger synchronization"""
    try:
        success = sync_service.sync_from_primary()
        if success:
            return JsonResponse({'message': 'Sync completed successfully'})
        else:
            return JsonResponse(
                {'message': 'Sync failed'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except Exception as e:
        return JsonResponse(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def aircraft_stats(request):
    """Get detailed aircraft statistics"""
    try:
        stats = {
            'total': Aircraft.objects.count(),
            'active': Aircraft.objects.filter(is_active=True).count(),
            'by_model': Aircraft.objects.values('model').annotate(
                count=Count('id')
            ).order_by('-count'),
            'recent_updates': Aircraft.objects.filter(
                last_updated__gte=timezone.now() - timedelta(minutes=5)
            ).count()
        }
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )