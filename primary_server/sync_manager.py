from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import os
import json

class FTPSync:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user("user", "12345", ".", perm="elradfmw")
        
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        
        self.server = FTPServer(("0.0.0.0", 2121), self.handler)
    
    def start(self):
        self.server.serve_forever()

def sync_data():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_to_backup, 'interval', minutes=5)
    scheduler.start()

def sync_to_backup():
    from .models import AircraftData
    data = AircraftData.objects.all()
    
    # Create JSON file with current data
    sync_data = [{'aircraft_id': item.aircraft_id,
                  'model': item.model,
                  'altitude': item.altitude,
                  'speed': item.speed,
                  'latitude': item.latitude,
                  'longitude': item.longitude,
                  'timestamp': str(item.timestamp)} for item in data]
    
    with open('sync_data.json', 'w') as f:
        json.dump(sync_data, f)
    
    # TODO: Implement FTP transfer to backup server 