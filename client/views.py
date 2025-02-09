import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response

PRIMARY_SERVER = 'http://primary-server:8000'
BACKUP_SERVER = 'http://backup-server:8000'

@login_required
def dashboard(request):
    return render(request, 'client/dashboard.html')

@api_view(['GET'])
def get_aircraft_data(request):
    try:
        # Try primary server first
        response = requests.get(f'{PRIMARY_SERVER}/api/aircraft/')
        if response.status_code == 200:
            return Response(response.json())
        
        # Fallback to backup server
        response = requests.get(f'{BACKUP_SERVER}/api/aircraft/')
        return Response(response.json())
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500) 