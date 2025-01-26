from django.db import models

class Aircraft(models.Model):
    aircraft_id = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=100)
    altitude = models.FloatField()
    speed = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aircraft_id} - {self.model}"

class ServerStatus(models.Model):
    is_active = models.BooleanField(default=True)
    last_heartbeat = models.DateTimeField(auto_now=True)
    server_type = models.CharField(max_length=20, default='PRIMARY')

    def __str__(self):
        return f"Server Status: {'Active' if self.is_active else 'Inactive'}" 