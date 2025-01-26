from django.apps import AppConfig

class BackupServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backup_server'

    def ready(self):
        from . import scheduler
        scheduler.start() 