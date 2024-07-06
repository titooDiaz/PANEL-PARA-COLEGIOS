from django import forms
from informacion.models import Actividades, Archivo

class ActividadesForm(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['titulo', 'descripcion', 'tipo', 'porcentaje', 'fecha_inicio', 'fecha_final', 'hora_inicio', 'hora_final']
        widgets = {
            'titulo': forms.TextInput(attrs={'autocomplete': 'off','id':'titulo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo de la actividad'}),

            'descripcion': forms.TextInput(attrs={'autocomplete': 'off','id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion de la actividad'}),
            
            'porcentaje': forms.NumberInput(attrs={'autocomplete': 'off','id':'porcentaje','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'porcentaje de la actividad', 'min': 1, 'max': 100}),

            'tipo': forms.Select(attrs={'id':'tipo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            
            'hora_inicio': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            
            'fecha_inicio': forms.DateInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ArchivoForm(forms.Form):
    archivo = forms.FileField(widget=forms.ClearableFileInput())