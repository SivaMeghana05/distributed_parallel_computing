from django.db import models

class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Inactive', 'Inactive'),
    ]

    aircraft_id = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aircraft_id} - {self.model}"

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.IntegerField()
    status = models.CharField(max_length=20)
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"Flight {self.flight_number} ({self.departure} → {self.arrival})"
