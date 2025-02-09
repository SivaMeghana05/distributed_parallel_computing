from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import timedelta

def generate_aircraft_id():
    return f"AC{uuid.uuid4().hex[:6].upper()}"

def generate_flight_number():
    return f"FLT{uuid.uuid4().hex[:6].upper()}"

class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    ]

    aircraft_id = models.CharField(max_length=50, unique=True, default=generate_aircraft_id)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aircraft_id} - {self.model}"

class Flight(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance')
    ]
    
    flight_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flight_number} - {self.status}"

class FlightTrack(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='flight_tracks')
    flight_number = models.CharField(max_length=20, unique=True, default=generate_flight_number)
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField(default=timezone.now)
    arrival_time = models.DateTimeField(null=True, blank=True)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    current_altitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Flight {self.flight_number}: {self.aircraft.aircraft_id}"

class UserProfile(models.Model):
    USER_TYPES = [
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='viewer')
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class MaintenanceSchedule(models.Model):
    MAINTENANCE_TYPES = [
        ('routine', 'Routine Check'),
        ('repair', 'Repair'),
        ('overhaul', 'Overhaul'),
        ('inspection', 'Inspection'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='maintenance_schedules')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    description = models.TextField()
    scheduled_date = models.DateTimeField()
    estimated_duration = models.DurationField(default=timedelta(hours=4))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    technician_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aircraft.aircraft_id} - {self.get_maintenance_type_display()} on {self.scheduled_date.date()}"

class PerformanceMetric(models.Model):
    METRIC_TYPES = [
        ('fuel_efficiency', 'Fuel Efficiency'),
        ('flight_time', 'Flight Time'),
        ('delays', 'Delays'),
        ('maintenance_cost', 'Maintenance Cost'),
    ]
    
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='performance_metrics')
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    date_recorded = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.aircraft.aircraft_id} - {self.get_metric_type_display()}: {self.value} {self.unit}"