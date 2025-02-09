from rest_framework import serializers
from .models import AircraftData

class AircraftDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftData
        fields = ['aircraft_id', 'model', 'altitude', 'speed', 
                 'latitude', 'longitude', 'timestamp', 'last_updated'] 