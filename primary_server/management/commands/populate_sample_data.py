from django.core.management.base import BaseCommand
from primary_server.models import Flight, Aircraft
import random
from datetime import datetime

class Command(BaseCommand):
    help = 'Populates the database with sample flight and aircraft data'

    def handle(self, *args, **kwargs):
        # Sample airports with coordinates
        airports = [
            ('JFK', 40.6413, -73.7781),
            ('LAX', 33.9416, -118.4085),
            ('ORD', 41.9742, -87.9073),
            ('LHR', 51.4700, -0.4543),
            ('CDG', 49.0097, 2.5479),
        ]

        # Create sample aircraft
        manufacturers = ['Boeing', 'Airbus']
        models = {
            'Boeing': ['737', '777', '787'],
            'Airbus': ['A320', 'A330', 'A350']
        }
        
        for i in range(10):
            manufacturer = random.choice(manufacturers)
            model = random.choice(models[manufacturer])
            Aircraft.objects.create(
                aircraft_id=f'AC{str(i+1).zfill(3)}',
                registration=f'N{random.randint(1000, 9999)}',
                manufacturer=manufacturer,
                model=model,
                year_manufactured=random.randint(2000, 2023),
                status=random.choice(['active', 'active', 'active', 'maintenance'])
            )

        # Create sample flights
        for i in range(5):
            origin, dest = random.sample(airports, 2)
            progress = random.random()
            
            current_lat = origin[1] + (dest[1] - origin[1]) * progress
            current_lon = origin[2] + (dest[2] - origin[2]) * progress

            Flight.objects.create(
                flight_number=f'FL{random.randint(100, 999)}',
                origin=origin[0],
                destination=dest[0],
                status='active',
                current_lat=current_lat,
                current_lon=current_lon,
                origin_lat=origin[1],
                origin_lon=origin[2],
                destination_lat=dest[1],
                destination_lon=dest[2]
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data')) 