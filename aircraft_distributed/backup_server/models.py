from django.db import models

class Aircraft(models.Model):
    aircraft_id = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    altitude = models.FloatField()
    speed = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.aircraft_id} - {self.model}" 