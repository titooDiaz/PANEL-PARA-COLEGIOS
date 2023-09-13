from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUserAlumno

class CustomUserAlumnoForm(UserCreationForm):
    class Meta:
        model = CustomUserAlumno
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'foto', 'tipo_documento', 'descripcion', 'introduccion', 'numero_documento', 'tipo_usuario', 'grado', 'sexo', 'estado', 'alergias', 'condiciones_medicas', 'medicamentos_actuales', 'grupo_sanguineo', 'contacto_emergencia_nombre', 'contacto_emergencia_telefono', 'ver_notas')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los widgets o agrega campos adicionales si es necesario
