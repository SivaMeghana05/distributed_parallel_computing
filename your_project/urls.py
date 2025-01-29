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
    # ... other paths ...
] 