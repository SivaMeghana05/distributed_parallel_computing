from rest_framework import serializers
from .models import Aircraft, FlightTrack

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['aircraft_id', 'model', 'manufacturer', 'status', 'last_updated']

class FlightTrackSerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(read_only=True)
    
    class Meta:
        model = FlightTrack
        fields = ['flight_number', 'aircraft', 'departure_location', 'arrival_location', 
                 'departure_time', 'arrival_time', 'current_latitude', 'current_longitude', 
                 'current_altitude'] 