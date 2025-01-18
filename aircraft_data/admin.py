from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Aircraft, FlightTrack, UserProfile, MaintenanceSchedule, PerformanceMetric

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_id', 'model', 'manufacturer', 'status', 'last_updated')
    list_filter = ('status', 'manufacturer')
    search_fields = ('aircraft_id', 'model', 'manufacturer')
    readonly_fields = ('last_updated',)

@admin.register(FlightTrack)
class FlightTrackAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'aircraft', 'departure_location', 'arrival_location')
    list_filter = ('departure_location', 'arrival_location')
    search_fields = ('flight_number', 'aircraft__aircraft_id', 'departure_location', 'arrival_location')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('aircraft', 'maintenance_type', 'scheduled_date', 'status')
    list_filter = ('maintenance_type', 'status', 'scheduled_date')
    search_fields = ('aircraft__aircraft_id', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ('aircraft', 'metric_type', 'value', 'unit', 'date_recorded')
    list_filter = ('metric_type', 'date_recorded')
    search_fields = ('aircraft__aircraft_id', 'notes')