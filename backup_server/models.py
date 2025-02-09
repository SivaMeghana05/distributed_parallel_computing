from django.db import models

<<<<<<< HEAD
class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='active')
    
    def __str__(self):
        return self.flight_number 
=======
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
>>>>>>> c4ec21ac5d79b78b3a800f51e8f415bbf2eac1bf
