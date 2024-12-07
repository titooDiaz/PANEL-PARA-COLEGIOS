from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import School
from django.forms import ClearableFileInput
from .models import CustomUserManager
from django.contrib.auth.forms import UserCreationForm


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(LoginForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'password'}),
    )


#Translate: ColegioForm
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['clave', 'colegio', 'numero', 'direccion', 'descripcion', 'cords', 'foto', 'banner']
        widgets = {
            'cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            'clave': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre Clave',"id":"clave"}),
            'colegio': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del colegio',"id":"colegio"}),
            'numero': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero de contacto',"id":"numero"}),
            'direccion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Direccion del colegio',"id":"direccion"}),
            'descripcion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion del colegio',"id":"descripcion"}),
            'foto': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),
            'banner': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5","id":"input-file-banner", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file-banner"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
#Translate: CustomUserGestorForm
class CustomUserManagerForm(UserCreationForm):
    class Meta:
        model = CustomUserManager
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'sexo','password1','password2', 'colegio')

        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off','id':'username','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero del documento'}),

            'first_name': forms.TextInput(attrs={'autocomplete': 'off','id':'first_name','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombres del usuario'}),

            'last_name': forms.TextInput(attrs={'id':'last_name','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Apellidos del usuario'}),

            'tipo_documento': forms.Select(attrs={'id':'tipo_documento','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'password': forms.TextInput(attrs={
                'id': 'password',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Contraseña',
                'autocomplete': 'current-password',
                'value': 'mkdj*F2023',
            }),

            'password1': forms.TextInput(attrs={'id': 'password1','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Contraseña'}),

            'password2': forms.TextInput(attrs={'id': 'password2','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Contraseña'}),

            'email': forms.EmailInput(attrs={'autocomplete': 'off','id':'email','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Email donde se puede contactar al usuario'}),

            'sexo': forms.Select(attrs={'id':'sexo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            
            'colegio': forms.Select(attrs={'id':'sexo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)