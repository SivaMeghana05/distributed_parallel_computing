from django import forms
from .models import Aircraft

class AircraftForm(forms.ModelForm):
    class Meta:
        model = Aircraft
        fields = ['name', 'model', 'manufacturer', 'year_manufactured', 'status']
