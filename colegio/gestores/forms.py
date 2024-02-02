from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUserGestor, CustomUserAlumno, CustomUserProfesores, CustomUserAdministrador, CustomUserAcudiente
from informacion.models import Grado, Horarios_Partes, Materias
#MENEJO DE ERRORES CON BASE DE DATOS
# COMPROBAR SI HAY TABLAS O LA BASE DE DATOS ESTA VACIA...
from django.db import connection

def obtener_tablas():
    engine = connection.settings_dict['ENGINE']
    if 'sqlite' in engine:
        # SQLite
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [table[0] for table in cursor.fetchall()]
    elif 'postgresql' in engine:
        # PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            return [table[0] for table in cursor.fetchall()]
    else:
        raise NotImplementedError(f"No se implementó soporte para el motor de base de datos {engine}")
tablas_en_bd = obtener_tablas()
#ALGUNAS PARTES DE ESTE FORMULARIO ENCESITAS LLAMAR A LOS ESTUDIANTES, PERO ES UN PROBLEMA, YA QUE SI NO TENEMOS BASE DE DATOS PODRIAMOS OBTENER ERRORES
#POR ESO AGREGAMOS ESTA FUNCION, NOS COMPRUEBA SI HAY O NO TABLAS EN NUESTRA BASE DE DATOS, SI NO HAY TABLAS SE SALTA LASZ FUNCIONES MIENTRAS SE HACEN MIGRACIONES PARA EVITAR ERRORES

class CustomUserAlumnoForm(UserCreationForm):
    class Meta:
        model = CustomUserAlumno
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'grado', 'sexo','password1','password2')

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

            'grado': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'sexo': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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


class CustomUserAdministradorForm(UserCreationForm):
    class Meta:
        model = CustomUserAdministrador
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento','sexo','password1','password2', 'introduccion','cargo')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero De Documento'}),

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

            'introduccion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion'}),

            'cargo': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserProfesoresForm(UserCreationForm):
    class Meta:
        model = CustomUserProfesores
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'titular', 'sexo','password1','password2', 'descripcion')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero De Documento'}),

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

            'titular': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'sexo': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'descripcion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomUserAcudienteForm(UserCreationForm):
    class Meta:
        if tablas_en_bd:
            choices = CustomUserAlumno.objects.all()
        else:
            choices = []
        model = CustomUserAcudiente
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento','password1','password2', 'introduccion', 'estudiante','sexo')

        widgets = {
            
            'estudiante': forms.CheckboxSelectMultiple(choices=choices,attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-orange-600 block w-20 p-2.5 estudiantes', 'placeholder': 'estudiante', 'id':'checkbox'}),

            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero De Documento'}),

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


class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        #fields = '__all__' 
        fields = ('grado_nom', 'grado_num', 'descripcion', 'horario_partes')
        widgets = {
             'grado_nom': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Grado Nom'}),

             'grado_num': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo1'}),

             'descripcion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion1'}),

             'horario_partes': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Horarios_PartesForm(forms.ModelForm):
    class Meta:
        model = Horarios_Partes
        fields = ('titulo', 'descripcion', 'horas')
        opciones_horas = [(i, f'{i} horas') for i in range(3, 23)]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del Horario'}),
            'descripcion': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Este horario...'}),
            'horas': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}, choices=opciones_horas),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class MateriasForm(forms.ModelForm):
    def __init__(self, *args, estudiantes_grado=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra los estudiantes por los proporcionados
        if estudiantes_grado:
            self.fields['alumnos1'].queryset = estudiantes_grado
            self.fields['alumnos2'].queryset = estudiantes_grado
    class Meta:
        model = Materias
        fields = ['profe1', 'profe2', 'electiva', 'titulo1', 'descripcion1', 'alumnos1', 'titulo2', 'descripcion2', 'alumnos2']
        widgets = {
            'profe1': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'profe2': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'electiva': forms.CheckboxInput(attrs={'class': 'w-12 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 focus:ring-2', 'id':'Checkbox'}),

            'titulo1': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo1'}),

            'descripcion1': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion1'}),

            'alumnos1': forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-orange-600 block w-20 p-2.5', 'placeholder': 'alumnos1', 'id':'checkbox'}),

            'titulo2': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo2'}),

            'descripcion2': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion2'}),

            'alumnos2': forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-orange-600 block w-20 p-2.5', 'placeholder': 'alumnos2', 'id':'checkbox'}),
            }
        

class CustomUserAdministradorForm(UserCreationForm):
    class Meta:
        model = CustomUserAdministrador
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'sexo','password1','password2', 'cargo')

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

            'cargo': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Cargo del usuario'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)