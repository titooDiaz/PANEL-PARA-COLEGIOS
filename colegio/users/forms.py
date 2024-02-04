from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import Colegio
from django.forms import ClearableFileInput


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(LoginForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'password'}),
    )
    
class ColegioForm(forms.ModelForm):
    class Meta:
        model = Colegio
        fields = ['clave', 'colegio', 'numero', 'direccion', 'descripcion', 'cords', 'foto', 'banner']
        widgets = {
            'cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            'clave': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre Clave',"id":"clave"}),
            'colegio': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del colegio',"id":"colegio"}),
            'numero': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero de contacto',"id":"numero"}),
            'direccion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Direccion del colegio',"id":"direccion"}),
            'descripcion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion del colegio',"id":"descripcion"}),
            'foto': ClearableFileInput(attrs={ "class":"block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),
            'banner': ClearableFileInput(attrs={ "class":"block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5","id":"input-file-banner", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file-banner"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)