from django import forms
from allauth.account.forms import LoginForm
from django.forms import ClearableFileInput
from .models import *
from django.contrib.auth.forms import UserCreationForm

# change password
from django.contrib.auth.forms import PasswordChangeForm


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
        fields = ['key_name', 'name', 'number', 'address', 'description', 'photo_cords', 'photo', 'banner']
        widgets = {
            'photo_cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            'key_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre Clave',"id":"key_name"}),
            'name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del colegio',"id":"name"}),
            'number': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero de contacto',"id":"number"}),
            'address': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Direccion del colegio',"id":"address"}),
            'description': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion del colegio',"id":"description"}),
            'photo': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),
            'banner': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5","id":"input-file-banner", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file-banner"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
#Translate: CustomUserGestorForm
class CustomUserManagerForm(UserCreationForm):
    class Meta:
        model = CustomUserManager
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'document_type', 'gender','password1','password2', 'school')

        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off','id':'username','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero del documento'}),

            'first_name': forms.TextInput(attrs={'autocomplete': 'off','id':'first_name','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombres del usuario'}),

            'last_name': forms.TextInput(attrs={'id':'last_name','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Apellidos del usuario'}),

            'document_type': forms.Select(attrs={'id':'tipo_documento','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

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

            'gender': forms.Select(attrs={'id':'sexo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            
            'school': forms.Select(attrs={'id':'school','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# change password
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': self.fields[field_name].label,
                'autocomplete': 'off'
            })

class CustomUserEditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
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
