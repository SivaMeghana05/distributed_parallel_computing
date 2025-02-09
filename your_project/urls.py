<<<<<<< HEAD
from django.urls import include, path, get_resolver
from django.contrib import admin
from primary_server.views import flight_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('primary_server.urls')),
    path('test_flights/', flight_list, name='test_flights'),  # Now flight_list is defined
=======
from django.urls import include, path
from accounts import views
from django.contrib import admin

urlpatterns = [
    path('primary_server/', include('primary_server.urls')),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
>>>>>>> c4ec21ac5d79b78b3a800f51e8f415bbf2eac1bf
    # ... other paths ...
]

print("Main URL patterns loaded")
urls = get_resolver().url_patterns
for url in urls:
    print(url) 
