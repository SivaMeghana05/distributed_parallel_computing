from django.shortcuts import render

def aircraft_list(request):
    # Your view logic here
    return render(request, 'aircraft_data/aircraft_list.html') 