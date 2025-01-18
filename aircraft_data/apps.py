from django.apps import AppConfig

class AircraftDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aircraft_data'

    # Start the scheduler when the app is ready
    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()

