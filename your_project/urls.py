from django.urls import include, path, get_resolver
from django.contrib import admin
from primary_server.views import flight_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('primary_server.urls')),
    path('test_flights/', flight_list, name='test_flights'),  # Now flight_list is defined
    # ... other paths ...
]

print("Main URL patterns loaded")
urls = get_resolver().url_patterns
for url in urls:
    print(url) 
