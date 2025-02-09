from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from aircraft_data.models import Flight

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@require_http_methods(['GET', 'POST'])
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def dashboard_view(request):
    active_flights = Flight.objects.filter(status='active')
    inactive_flights = Flight.objects.filter(status='inactive')
    maintenance_flights = Flight.objects.filter(status='maintenance')
    
    context = {
        'active_flights': active_flights,
        'inactive_flights': inactive_flights,
        'maintenance_flights': maintenance_flights,
    }
    return render(request, 'accounts/dashboard.html', context)