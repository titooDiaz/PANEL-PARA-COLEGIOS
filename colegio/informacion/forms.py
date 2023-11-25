from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HorarioDiario

class HoraHorarioForm(forms.ModelForm):
    class Meta:
        model = HorarioDiario
        fields = ('hora_inicio', 'hora_fin', 'Hora')

        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-input'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-input'}),
            'Hora': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)