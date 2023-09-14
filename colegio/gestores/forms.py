from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUserGestor

class CustomUserGestorForm(UserCreationForm):
    class Meta:
        model = CustomUserGestor
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'sexo','password1','password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del usuario'}),

            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombres del usuario'}),

            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Apellidos del usuario'}),

            'tipo_documento': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'password': forms.TextInput(attrs={
                'id': 'password',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Contraseña',
                'autocomplete': 'current-password',
                'value': 'mkdj*F2023',
            }),

            'password1': forms.TextInput(attrs={'id': 'password1','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Contraseña'}),

            'password2': forms.TextInput(attrs={'id': 'password2','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Contraseña'}),

            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Email donde se puede contactar al usuario'}),

            'sexo': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)