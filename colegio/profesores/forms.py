from django import forms
from informacion.models import Actividades, Archivo, ActividadesTipo
from django.forms.widgets import DateInput, TimeInput


class FilesProfesoresForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['archivo', 'nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'autocomplete': 'off','id':'nombre','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo de la actividad'}),
            
            'descripcion': forms.TextInput(attrs={'autocomplete': 'off','id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripccion del documento de la actividad'}),
            
            'archivo': forms.FileInput(attrs={'id':'archivo', 'class': 'hidden'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ActividadesForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    class Meta:
        model = Actividades
        fields = ['titulo', 'descripcion', 'tipo', 'porcentaje', 'fecha_inicio', 'fecha_final', 'hora_inicio', 'hora_final', 'zona_horaria', 'lugar_zona_horaria']
        widgets = {
            'titulo': forms.TextInput(attrs={'autocomplete': 'off','id':'titulo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo de la actividad'}),
            
            'lugar_zona_horaria': forms.TextInput(attrs={'autocomplete': 'off','id':'lugar_zona_horaria','class': 'hidden'}),

            'descripcion': forms.TextInput(attrs={'autocomplete': 'off','id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion de la actividad'}),
            
            'porcentaje': forms.NumberInput(attrs={'autocomplete': 'off','id':'porcentaje','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'porcentaje de la actividad', 'min': 1, 'max': 100}),

            'tipo': forms.Select(attrs={'id':'tipo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            
            'hora_inicio': forms.TimeInput(attrs={'id':'hora_inicio','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            
            'fecha_inicio': forms.DateInput(attrs={'id':'fecha_inicio','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),
            
            'hora_final': forms.TimeInput(attrs={'id':'hora_final','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            
            'fecha_final': forms.DateInput(attrs={'id':'fecha_final','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),

            'zona_horaria': forms.CheckboxInput(attrs={'id':'zona_horaria','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300 focus:ring-orange-600 w-full h-12',}),

        }


class ArchivoForm(forms.Form):
    archivo = forms.FileField(widget=forms.ClearableFileInput())
