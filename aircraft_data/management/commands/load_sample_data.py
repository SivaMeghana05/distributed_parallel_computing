from django.core.management.base import BaseCommand
from aircraft_data.models import Aircraft, FlightTrack
from django.utils import timezone

class Command(BaseCommand):
    help = 'Loads sample aircraft data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Aircraft.objects.all().delete()
        FlightTrack.objects.all().delete()

        # Create sample aircraft
        aircraft1 = Aircraft.objects.create(
            model='Boeing 737',
            manufacturer='Boeing',
            status='active'
        )

        aircraft2 = Aircraft.objects.create(
            model='Airbus A320',
            manufacturer='Airbus',
            status='active'
        )

        aircraft3 = Aircraft.objects.create(
            model='F-16 Fighting Falcon',
            manufacturer='Lockheed Martin',
            status='maintenance'
        )

        # Create sample flight tracks
        FlightTrack.objects.create(
            aircraft=aircraft1,
            departure_location='New Delhi',
            arrival_location='Mumbai',
            departure_time=timezone.now(),
            current_latitude=28.6139,
            current_longitude=77.2090,
            current_altitude=30000,
            is_completed=False
        )

        FlightTrack.objects.create(
            aircraft=aircraft2,
            departure_location='Bangalore',
            arrival_location='Chennai',
            departure_time=timezone.now(),
            current_latitude=12.9716,
            current_longitude=77.5946,
            current_altitude=25000,
            is_completed=False
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data')) 