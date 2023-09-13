from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUserAlumno

class CustomUserAlumnoForm(UserCreationForm):
    class Meta:
        model = CustomUserAlumno
        fields = ('username', 'first_name', 'last_name', 'email', 'password','tipo_documento', 'grado', 'sexo')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5', 'placeholder': 'Nombre del usuario'}),

            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5', 'placeholder': 'Apellido del usuario'}),

            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5', 'placeholder': 'Numero de telefono del usuario'}),


            'tipo_documento': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5'}),

            'password': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5', 'placeholder': 'Numero de telefono del usuario'}),

            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5', 'placeholder': 'Email donde se puede contactar al usuario'}),

            'grado': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5'}),

            'sexo': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
