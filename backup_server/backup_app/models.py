from django.db import models

# Create your models here.

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    current_altitude = models.IntegerField(default=0)
    current_latitude = models.FloatField(default=0.0)
    current_longitude = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='active')
    
    def __str__(self):
        return self.flight_number

    class Meta:
        db_table = 'aircraft_data_flight'  # Updated table name
        managed = False  # Don't create/modify the table
