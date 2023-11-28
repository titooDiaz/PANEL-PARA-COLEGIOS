from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HorarioDiario

class HoraHorarioForm(forms.ModelForm):
    class Meta:
        model = HorarioDiario
        fields = ('hora_inicio', 'hora_fin')

        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
    'hora_fin': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)