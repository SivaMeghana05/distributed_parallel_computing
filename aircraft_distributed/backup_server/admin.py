from django.contrib import admin
from .models import Aircraft
from .sync_service import sync_service

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_id', 'model', 'altitude', 'speed', 'latitude', 'longitude', 'last_updated', 'is_active')
    list_filter = ('is_active', 'model')
    search_fields = ('aircraft_id', 'model')
    readonly_fields = ('last_updated',)
    
    def changelist_view(self, request, extra_context=None):
        # Add sync status to the admin view
        extra_context = extra_context or {}
        sync_status = sync_service.get_last_sync_status()
        extra_context['sync_status'] = sync_status
        return super().changelist_view(request, extra_context=extra_context)

    actions = ['force_sync']

    @admin.action(description='Force sync with primary server')
    def force_sync(self, request, queryset):
        success = sync_service.sync_from_primary()
        if success:
            self.message_user(request, "Successfully synced with primary server")
        else:
            self.message_user(request, "Sync failed. Check logs for details", level='ERROR') 