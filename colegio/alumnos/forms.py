from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUserAlumno
from django.contrib.auth.forms import AuthenticationForm

class CustomUserAlumnoForm(UserCreationForm):
    class Meta:
        model = CustomUserAlumno
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'foto', 'tipo_documento', 'descripcion', 'introduccion', 'numero_documento', 'tipo_usuario', 'grado', 'sexo', 'estado', 'alergias', 'condiciones_medicas', 'medicamentos_actuales', 'grupo_sanguineo', 'contacto_emergencia_nombre', 'contacto_emergencia_telefono', 'ver_notas')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los widgets o agrega campos adicionales si es necesario

class CustomAlumnoLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)




