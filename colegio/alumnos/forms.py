from django import forms
from informacion.models import StudentResponse

#Translate: ActividadesRespuestaForm
class ActivitiesAnswerForm(forms.ModelForm):
    class Meta:
        model = StudentResponse
        fields = ['answer', 'description']  # OJO NUESTRO ELEMENTO ARCIVO ESTARA EN LAVISTA HTML!
        widgets = {
            'answer': forms.TextInput(attrs={
                'id': 'respuesta',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Este archivo es...'
            }),
            'description': forms.TextInput(attrs={
                'id': 'descripcion',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Escribe aquí tu descripción'
            }),
        }