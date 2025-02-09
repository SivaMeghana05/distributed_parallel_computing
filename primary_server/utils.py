import requests
from django.conf import settings

def sync_to_backup_server(data, endpoint):
    """
    Synchronize data to the backup server
    """
    try:
        # You'll need to set this in settings.py
        backup_server_url = getattr(settings, 'BACKUP_SERVER_URL', 'http://localhost:8001')
        
        # Construct the full URL
        url = f"{backup_server_url}/api/{endpoint}/"
        
        # Make the request to the backup server
        response = requests.post(url, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            return True, "Successfully synced to backup server"
        else:
            return False, f"Failed to sync: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Error syncing to backup server: {str(e)}" 