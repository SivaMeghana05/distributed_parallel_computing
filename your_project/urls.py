from django.urls import include, path

urlpatterns = [
    path('primary_server/', include('primary_server.urls')),
    # ... other paths ...
] 