from django import forms
from informacion.models import StudentResponse

class ActividadesRespuestaForm(forms.ModelForm):
    class Meta:
        model = StudentResponse
        fields = ['respuesta', 'descripcion']  # OJO NUESTRO ELEMENTO ARCIVO ESTARA EN LAVISTA HTML!
        widgets = {
            'respuesta': forms.TextInput(attrs={
                'id': 'respuesta',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Este archivo es...'
            }),
            'descripcion': forms.TextInput(attrs={
                'id': 'descripcion',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Escribe aquí tu descripción'
            }),
        }