import math
from datetime import datetime, timedelta

def calculate_current_position(flight):
    """Calculate current position of flight based on departure and arrival coordinates"""
    
    # Convert string coordinates to floats
    dep_lat = float(flight.departure_latitude)
    dep_lon = float(flight.departure_longitude)
    arr_lat = float(flight.arrival_latitude)
    arr_lon = float(flight.arrival_longitude)
    
    # Calculate flight duration and progress
    flight_duration = 2  # hours (simplified)
    time_elapsed = (datetime.now() - flight.departure_time.replace(tzinfo=None)).total_seconds() / 3600
    progress = min(time_elapsed / flight_duration, 1)
    
    # Calculate current position
    current_lat = dep_lat + (arr_lat - dep_lat) * progress
    current_lon = dep_lon + (arr_lon - dep_lon) * progress
    
    return {
        'latitude': current_lat,
        'longitude': current_lon,
        'altitude': 30000,  # Cruising altitude in feet
        'progress': progress * 100  # Progress percentage
    }

def get_flight_statistics():
    """Calculate overall flight statistics"""
    return {
        'total_distance': 0,  # To be implemented
        'average_duration': 0,  # To be implemented
        'on_time_percentage': 0,  # To be implemented
    } 