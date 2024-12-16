from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import DailySchedule
from users.models import CustomUserStudent

class HoraHorarioForm(forms.ModelForm):
    class Meta:
        model = DailySchedule
        fields = ('hora_inicio', 'hora_fin')

        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class MateriasHorarioForm(forms.ModelForm):
    def __init__(self, *args, materias_grado=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las materias dependientes de este grado
        if materias_grado:
            self.fields['lunes'].queryset = materias_grado
            self.fields['martes'].queryset = materias_grado
            self.fields['miercoles'].queryset = materias_grado
            self.fields['jueves'].queryset = materias_grado
            self.fields['viernes'].queryset = materias_grado
            print("hola")
            
    class Meta:
        model = DailySchedule
        fields = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
        widgets = {
            'lunes': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'martes': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'miercoles': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'jueves': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'viernes': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            }
        
class EditarVerNotasAlumnosForm(forms.ModelForm):
    class Meta:
        model = CustomUserStudent
        fields = ['see_notes']
        widgets = {
            'see_notes': forms.CheckboxInput(attrs={'class': 'h-8 w-8 m-0 text-blue-600 bg-gray-100 border-gray-300 rounded', 'id':'Checkbox'}),

            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        