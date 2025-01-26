import requests
from django.conf import settings
import logging
from datetime import datetime
from .models import Aircraft

logger = logging.getLogger(__name__)

class BackupSyncService:
    def __init__(self):
        self.primary_server_url = getattr(settings, 'PRIMARY_SERVER_URL', 'http://localhost:8000')
        self.last_sync_time = None

    def check_primary_server_health(self):
        """Check if primary server is responding"""
        try:
            response = requests.get(f"{self.primary_server_url}/primary/health/", timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Primary server health check failed: {str(e)}")
            return False

    def sync_from_primary(self):
        """Sync aircraft data from primary server"""
        try:
            response = requests.get(f"{self.primary_server_url}/primary/aircraft/", timeout=10)
            if response.status_code == 200:
                aircraft_data = response.json()
                
                for data in aircraft_data:
                    Aircraft.objects.update_or_create(
                        aircraft_id=data['aircraft_id'],
                        defaults={
                            'model': data['model'],
                            'altitude': data['altitude'],
                            'speed': data['speed'],
                            'latitude': data['latitude'],
                            'longitude': data['longitude'],
                            'is_active': True
                        }
                    )
                
                self.last_sync_time = datetime.now()
                logger.info(f"Sync completed successfully at {self.last_sync_time}")
                return True
        except requests.RequestException as e:
            logger.error(f"Sync failed: {str(e)}")
            return False

    def get_last_sync_status(self):
        """Get information about the last synchronization"""
        return {
            'last_sync_time': self.last_sync_time.isoformat() if self.last_sync_time else None,
            'primary_server_available': self.check_primary_server_health()
        }

# Create a global instance of the sync service
sync_service = BackupSyncService() 