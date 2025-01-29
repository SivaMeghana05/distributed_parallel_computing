from django.core.management.base import BaseCommand
from primary_server.models import Aircraft, Flight
from django.utils import timezone
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Load sample aircraft and flight data'

    def handle(self, *args, **kwargs):
        # Set a fixed timestamp for sample data
        sample_time = datetime(2025, 1, 17, 16, 20, tzinfo=pytz.UTC)  # 4:20 PM UTC

        # Create Aircraft data
        aircraft_data = [
            ('AC795FFF', 'Boeing 737', 'Boeing', 'Active', '16:20'),
            ('AC7B2B55', 'Airbus A320', 'Airbus', 'Active', '16:20'),
            ('AC37388D', 'F-16 Fighting Falcon', 'Lockheed Martin', 'Under Maintenance', '16:21'),
            ('ACB2E7DD', 'C-130 Hercules', 'Lockheed Martin', 'Active', '16:21'),
            ('AC21B24B', 'Dassault Rafale', 'Dassault Aviation', 'Active', '16:22'),
            ('ACF73435', 'Boeing 747', 'Boeing', 'Inactive', '16:22'),
            ('AC232B4B', 'Airbus A380', 'Airbus', 'Under Maintenance', '16:22'),
            ('AC5ECA84', 'MiG-29', 'Mikoyan', 'Inactive', '16:23'),
            ('ACFB4F35', 'Sukhoi Su-30MKI', 'Sukhoi', 'Under Maintenance', '16:23'),
            ('AC73ABE6', 'Boeing C-17', 'Boeing', 'Active', '16:23'),
        ]

        # Create Aircraft instances
        for aircraft_id, model, manufacturer, status, time in aircraft_data:
            hour, minute = map(int, time.split(':'))
            timestamp = datetime(2025, 1, 17, hour, minute, tzinfo=pytz.UTC)
            Aircraft.objects.create(
                aircraft_id=aircraft_id,
                model=model,
                manufacturer=manufacturer,
                status=status,
                last_updated=timestamp
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample aircraft data'))

        # Flight data can be added in a similar way if needed 