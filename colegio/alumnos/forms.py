from django import forms
from informacion.models import Actividades_Respuesta_Estudiantes

class ActividadesRespuestaForm(forms.ModelForm):
    class Meta:
        model = Actividades_Respuesta_Estudiantes
        fields = ['respuesta', 'descripcion', 'fecha_entrega', 'hora_entrega', 'lugar_zona_horaria', 'misma_zona', 'archivo']
        widgets = {
            'archivo': forms.FileInput(attrs={'id':'archivo', 'class': 'hidden'}),
            'hora_entrega': forms.TimeInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            'fecha_entrga': forms.DateInput(attrs={'id':'fecha_entrga','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),
            'respuesta': forms.TextInput(attrs={'id':'respuesta','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Este archivo es...'}),
            'descripcion': forms.TextInput(attrs={'id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Escribe aqui tu descripcion'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)