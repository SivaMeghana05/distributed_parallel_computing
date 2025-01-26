from django.db import models

class ServerStatus(models.Model):
    is_active = models.BooleanField(default=True)
    last_heartbeat = models.DateTimeField(auto_now=True)
    server_type = models.CharField(max_length=20, choices=[
        ('PRIMARY', 'Primary Server'),
        ('BACKUP', 'Backup Server')
    ])
    
    class Meta:
        verbose_name_plural = "Server Statuses"

class AircraftData(models.Model):
    aircraft_id = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=100)
    altitude = models.FloatField()
    speed = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Aircraft(models.Model):
    registration = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    year_manufactured = models.IntegerField()
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('retired', 'Retired')
    ])

    def __str__(self):
        return f"{self.registration} - {self.model}"

class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)  # Assuming you have a Flight model
    seat_number = models.CharField(max_length=5)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} for {self.flight.flight_number}"

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