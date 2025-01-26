from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .sync_service import sync_service
import logging

logger = logging.getLogger(__name__)

def start():
    try:
        scheduler = BackgroundScheduler()
        
        # Add sync job to run every 30 seconds
        scheduler.add_job(
            sync_service.sync_from_primary,
            'interval',
            seconds=30,
            id='sync_from_primary',
            replace_existing=True
        )
        
        # Add health check job to run every 15 seconds
        scheduler.add_job(
            sync_service.check_primary_server_health,
            'interval',
            seconds=15,
            id='check_primary_health',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("Scheduler started successfully")
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}") 