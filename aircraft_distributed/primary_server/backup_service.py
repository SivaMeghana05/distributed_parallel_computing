import requests
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BackupServerManager:
    def __init__(self):
        self.backup_server_url = getattr(settings, 'BACKUP_SERVER_URL', 'http://localhost:8001')
        self.last_backup_time = None
        self.backup_status = {
            'is_available': False,
            'last_sync_time': None,
            'sync_errors': 0,
            'consecutive_failures': 0
        }

    def check_backup_server(self):
        """Check if backup server is available"""
        try:
            response = requests.get(f"{self.backup_server_url}/backup/status/", timeout=5)
            self.backup_status['is_available'] = response.status_code == 200
            if self.backup_status['is_available']:
                self.backup_status['consecutive_failures'] = 0
            return self.backup_status['is_available']
        except requests.RequestException as e:
            logger.error(f"Backup server check failed: {str(e)}")
            self.backup_status['consecutive_failures'] += 1
            self.backup_status['is_available'] = False
            return False

    def sync_aircraft_data(self, aircraft_data):
        """Sync aircraft data to backup server"""
        if not self.check_backup_server():
            logger.warning("Backup server not available for sync")
            return False

        try:
            response = requests.post(
                f"{self.backup_server_url}/backup/sync/",
                json=aircraft_data,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                self.last_backup_time = datetime.now()
                self.backup_status['last_sync_time'] = self.last_backup_time
                logger.info(f"Successfully synced data to backup server at {self.last_backup_time}")
            else:
                self.backup_status['sync_errors'] += 1
                logger.error(f"Sync failed with status code: {response.status_code}")
            
            return success

        except requests.RequestException as e:
            self.backup_status['sync_errors'] += 1
            logger.error(f"Error syncing to backup server: {str(e)}")
            return False

    def get_backup_status(self):
        """Get current backup server status"""
        return {
            'is_available': self.backup_status['is_available'],
            'last_sync_time': self.backup_status['last_sync_time'].isoformat() 
                if self.backup_status['last_sync_time'] else None,
            'sync_errors': self.backup_status['sync_errors'],
            'consecutive_failures': self.backup_status['consecutive_failures']
        }

    def notify_aircraft_deletion(self, aircraft_id):
        """Notify backup server about aircraft deletion"""
        if not self.check_backup_server():
            return False

        try:
            response = requests.delete(
                f"{self.backup_server_url}/backup/delete/{aircraft_id}/",
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Failed to notify backup server about deletion: {str(e)}")
            return False

# Create a global instance
backup_manager = BackupServerManager() 