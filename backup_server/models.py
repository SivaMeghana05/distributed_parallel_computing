from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='active')
    
    def __str__(self):
        return self.flight_number 