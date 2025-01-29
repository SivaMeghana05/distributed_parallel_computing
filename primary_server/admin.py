from django.contrib import admin
from .models import Aircraft, Flight

# Register your models
@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_id', 'model', 'status')
    search_fields = ('aircraft_id', 'model')
    list_filter = ('status',)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'aircraft', 'departure', 'arrival', 'status', 'departure_time')
    search_fields = ('flight_number', 'departure', 'arrival')
    list_filter = ('status',) 