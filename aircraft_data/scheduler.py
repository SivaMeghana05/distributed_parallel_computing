from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

# Simulating fetching data from servers
def fetch_aircraft_data():
    print("Fetching aircraft data from servers...")

# Start and configure the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_aircraft_data,
        trigger=IntervalTrigger(minutes=5),  # Run every 5 minutes
        id="fetch_aircraft_data",  # Unique ID for the job
        replace_existing=True  # Replace job if it already exists
    )
    scheduler.start()
    logging.getLogger("apscheduler").setLevel(logging.DEBUG)
