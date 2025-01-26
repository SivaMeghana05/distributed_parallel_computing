from django.urls import path
from . import views

app_name = 'backup_server'

urlpatterns = [
    path('monitor/', views.monitor_dashboard, name='monitor_dashboard'),
    path('status/', views.server_status, name='server_status'),
    path('sync/', views.sync_aircraft_data, name='sync_aircraft_data'),
    path('aircraft/', views.get_all_aircraft, name='get_all_aircraft'),
    path('delete/<str:aircraft_id>/', views.delete_aircraft, name='delete_aircraft'),
] 