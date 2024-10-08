from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUserGestor, CustomUserAlumno, CustomUserProfesores, CustomUserAdministrador, CustomUserAcudiente
from informacion.models import Grado, Horarios_Partes, Materias, HorarioCortes, ActividadesTipo

#imagenes de usuarios
from django.forms import ClearableFileInput


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
    def __init__(self, *args, grado=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra Grados por el colegio del estudiante por agregar (usuario en sesion)
        if grado:
            self.fields['grado'].queryset = grado
    class Meta:
        model = CustomUserAlumno
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'grado', 'sexo','password1','password2','cords','foto', 'colegio', 'time_zone')

        widgets = {
            'time_zone': forms.TextInput(attrs={'id':'time_zone','class': 'hidden'}),
            
            'username': forms.TextInput(attrs={'id':'username','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del usuario','autocomplete':'off'}),

            'first_name': forms.TextInput(attrs={'id':'first_name','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombres del usuario','autocomplete':'off'}),

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

            'email': forms.EmailInput(attrs={'id':'email','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Email donde se puede contactar al usuario','autocomplete':'off'}),

            'grado': forms.Select(attrs={'id':'grado','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'sexo': forms.Select(attrs={'id':'sexo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            
            'cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            'foto': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),
            
        }

class CustomUserGestorForm(UserCreationForm):
    class Meta:
        model = CustomUserGestor
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'sexo','password1','password2', 'colegio','cords','foto', 'time_zone')

        widgets = {
            'time_zone': forms.TextInput(attrs={'id':'time_zone','class': 'hidden'}),
            'username': forms.TextInput(attrs={'autocomplete': 'off','id':'username','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del usuario'}),

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
            
            'cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            'foto': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserAdministradorForm(UserCreationForm):
    class Meta:
        model = CustomUserAdministrador
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento','sexo','password1','password2', 'introduccion','cargo', 'colegio','cords','foto', 'time_zone')

        widgets = {
            'time_zone': forms.TextInput(attrs={'id':'time_zone','class': 'hidden'}),
            
            'username': forms.TextInput(attrs={'autocomplete': 'off','id':'username','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero De Documento'}),

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

            'email': forms.EmailInput(attrs={'autocomplete': 'off', 'id':'email','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Email donde se puede contactar al usuario'}),

            'sexo': forms.Select(attrs={'id':'sexo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'introduccion': forms.TextInput(attrs={'id':'introduccion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion'}),

            'cargo': forms.TextInput(attrs={'id':'cargo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion'}),
            
            'cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            'foto': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserProfesoresForm(UserCreationForm):
    def __init__(self, *args, titular=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra Grados por el colegio del estudiante por agregar (usuario en sesion)
        if titular:
            self.fields['titular'].queryset = titular
    class Meta:
        model = CustomUserProfesores
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento', 'titular', 'sexo','password1','password2', 'descripcion', 'colegio','cords','foto', 'time_zone')

        widgets = {
            'time_zone': forms.TextInput(attrs={'id':'time_zone','class': 'hidden'}),
            
            'username': forms.TextInput(attrs={'autocomplete': 'off','id':'username','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero De Documento'}),

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

            'titular': forms.Select(attrs={'id':'titular','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'sexo': forms.Select(attrs={'id':'sexo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'descripcion': forms.TextInput(attrs={'id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion'}),
            
            'cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            'foto': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),
        }

class CustomUserAcudienteForm(UserCreationForm):
    def __init__(self, *args, estudiantes_colegio=None, **kwargs):
        super().__init__(*args, **kwargs)
        if estudiantes_colegio:
            self.fields['estudiante'].queryset = CustomUserAlumno.objects.filter(colegio=estudiantes_colegio)
    class Meta:
        model = CustomUserAcudiente
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'tipo_documento','password1','password2', 'introduccion', 'estudiante','sexo', 'colegio', 'time_zone')

        widgets = {
            'time_zone': forms.TextInput(attrs={'id':'time_zone','class': 'hidden'}),
            
            'estudiante': forms.CheckboxSelectMultiple(attrs={'id':'estudiante','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-orange-600 block w-20 p-2.5 estudiantes', 'placeholder': 'estudiante', 'id':'checkbox'}),

            'username': forms.TextInput(attrs={'id':'username','autocomplete': 'off','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero De Documento'}),

            'first_name': forms.TextInput(attrs={'id':'first_name','autocomplete': 'off','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombres del usuario'}),

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

            'email': forms.EmailInput(attrs={'id':'email','autocomplete': 'off','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Email donde se puede contactar al usuario'}),

            'sexo': forms.Select(attrs={'id':'sexo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }


class GradoForm(forms.ModelForm):
    def __init__(self, *args, horario_partes=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra los estudiantes por los proporcionados
        if horario_partes:
            self.fields['horario_partes'].queryset = Horarios_Partes.objects.filter(colegio=horario_partes)
    class Meta:
        model = Grado
        #fields = '__all__' 
        fields = ('grado_nom', 'grado_num', 'descripcion', 'horario_partes', 'colegio')
        widgets = {
             'grado_nom': forms.TextInput(attrs={'id':'grado_nom','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del grado'}),

             'grado_num': forms.TextInput(attrs={'id':'grado_num','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Numero de grado + letra'}),

             'descripcion': forms.TextInput(attrs={'id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion del grado'}),

             'horario_partes': forms.Select(attrs={'id':'horario_partes','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
        }


class Horarios_PartesForm(forms.ModelForm):
    class Meta:
        model = Horarios_Partes
        fields = ('titulo', 'descripcion', 'horas', 'cortes')
        opciones_horas = [(i, f'{i} horas') for i in range(3, 23)]
        opciones_corte = [(i, f'{i} cortes') for i in range(1, 7)]
        widgets = {
            'titulo': forms.TextInput(attrs={'id':'titulo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del Horario'}),
            'descripcion': forms.TextInput(attrs={'id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Este horario...'}),
            'horas': forms.Select(attrs={'id':'horas','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}, choices=opciones_horas),
            'cortes': forms.Select(attrs={'id':'cortes','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}, choices=opciones_corte),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class MateriasForm(forms.ModelForm):
    def __init__(self, *args, estudiantes_grado=None, profesores=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra los estudiantes por los proporcionados
        if estudiantes_grado:
            self.fields['profe1'].queryset = profesores
            self.fields['profe2'].queryset = profesores
            self.fields['alumnos1'].queryset = estudiantes_grado
            self.fields['alumnos2'].queryset = estudiantes_grado
    class Meta:
        model = Materias
        fields = ['profe1', 'picture1', 'cords', 'locate1', 'locate2', 'profe2', 'electiva', 'titulo1', 'descripcion1', 'alumnos1', 'titulo2', 'descripcion2', 'alumnos2']
        widgets = {
            'profe1': forms.Select(attrs={'id':'profe1','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),
            
            'picture1': ClearableFileInput(attrs={ "class":"block w-full text-lg text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 p-2.5", "id":"input-file", "type":"file","accept":".png,.jpg,.jpeg","name":"input-file"}),

            'profe2': forms.Select(attrs={'id':'profe2','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5'}),

            'electiva': forms.CheckboxInput(attrs={'class': 'w-12 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 focus:ring-2', 'id':'Checkbox'}),

            'titulo1': forms.TextInput(attrs={'id':'titulo1','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo1'}),

            'descripcion1': forms.TextInput(attrs={'id':'descripcion1','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion1'}),
            
            'locate1': forms.TextInput(attrs={'id':'locate1','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Ubicacion'}),


            'alumnos1': forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-orange-600 block w-20 p-2.5 ', 'placeholder': 'alumnos1', 'id':'checkbox_es_1'}),

            'titulo2': forms.TextInput(attrs={'id':'titulo2','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo2'}),

            'descripcion2': forms.TextInput(attrs={'id':'descripcion2','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion2'}),
            
            'locate2': forms.TextInput(attrs={'id':'locate2','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Ubicacion'}),

            'alumnos2': forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-orange-600 block w-20 p-2.5 ', 'placeholder': 'alumnos2', 'id':'checkbox_es_2'}),
            
            'cords': forms.TextInput(attrs={'class': 'cords hidden', 'id':'cords'}),
            }

class HorarioCortesForm(forms.ModelForm):
    class Meta:
        model = HorarioCortes
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'id':'fecha_inicio','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),
            'fecha_fin': forms.DateInput(attrs={'id':'fecha_inicio','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),
        }
        
class ActividadesTipoForm(forms.ModelForm):
    class Meta:
        model = ActividadesTipo
        fields = ('titulo', 'descripcion')
        widgets = {
            'titulo': forms.TextInput(attrs={'id':'titulo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Nombre del Horario'}),
            'descripcion': forms.TextInput(attrs={'id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5', 'placeholder': 'Este horario...'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)