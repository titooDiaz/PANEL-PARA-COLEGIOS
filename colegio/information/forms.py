from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import DailySchedule
from users.models import CustomUserStudent

class HoraHorarioForm(forms.ModelForm):
    class Meta:
        model = DailySchedule
        fields = ('start_time', 'end_time')

        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class MateriasHorarioForm(forms.ModelForm):
    def __init__(self, *args, materias_grado=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las materias dependientes de este grado
        if materias_grado:
            self.fields['monday'].queryset = materias_grado
            self.fields['tuesday'].queryset = materias_grado
            self.fields['wednesday'].queryset = materias_grado
            self.fields['thursday'].queryset = materias_grado
            self.fields['friday'].queryset = materias_grado
            self.fields['saturday'].queryset = materias_grado
            print("hola")
            
    class Meta:
        model = DailySchedule
        fields = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        widgets = {
            'monday': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'tuesday': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'wednesday': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'thursday': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'friday': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            'saturday': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
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
        