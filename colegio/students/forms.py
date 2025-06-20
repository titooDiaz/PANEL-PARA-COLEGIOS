from django import forms
from information.models import *

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

class CustomUserStudentEditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUserStudent
        fields = ('first_name', 'last_name', 'email')
        widgets = {  
            'first_name': forms.TextInput(attrs={
                'autocomplete': 'off',
                'id': 'first_name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Nombres del usuario'
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'last_name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Apellidos del usuario'
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'off',
                'id': 'email',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Email donde se puede contactar al usuario'
            }),
        }        