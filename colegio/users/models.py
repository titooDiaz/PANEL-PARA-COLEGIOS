from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings # usar los settings
from django.db import models
import os
from django.utils import timezone
import re

##########################START CUSTOM USER###################################
SEXO = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Sin informacion', 'Sin informacion'),
    ]
TIPO_USUARIO = [
        ('Profesor', 'Profesor'),
        ('Acudiente', 'Acudiente'),
        ('Alumno', 'Alumno'),
        ('Gestor', 'Gestor'),
        ('Administrador', 'Administrador'),
    ]
TIPO_DOCUMENTO=[
        ('Sin Informacion', 'Sin Informacion'),
        ('Tarjeta de Identidad','Tarjeta de Identidad'),
        ('Cédula de Ciudadanía','Cédula de Ciudadanía'),
        ('Cédula de Extranjería', 'Cédula de Extranjería'),
        ('Registro Civil de Nacimiento','Registro Civil de Nacimiento'),
        ('Permiso Especial de Permanencia','Permiso Especial de Permanencia'),
    ]
TIPO_SANGRE = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('Desconocido', 'Desconocido'),
    ]




#A SIMPLE VISTA NO PARECE TENER SENTIDO COLOCAR EL COLEGIO EN USUARIOS, PERO DEBEMOS PENSAR QUE LA CARACTERISTICA PRINCIPAL DE LOS USUARIOS ES QUE PERTENENCEN A UN COLEGIO
#POR ESO DECIDIMOS COLOCAR EL MODELO EN ESTA APLICACION. CAMBIARLA A INFORMACION PUEDE TRAER ALGUNOS CONFLICTOS, ASI QUE EL COLEGIO FUNCIONA CORRECTAMENTE ACA! NO LO MUEVAS.
#MOVERLO A INFORMACION PODRIA PROVOCAR UNA RELACION INVERSA.
def colegio_directory_path_profile(instance, filename):
    # el cero es el format
    profile_picture_name = 'colegiosFoto/media/{0}/profile.png'.format(instance.key_name)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

def colegio_directory_path_banner(instance, filename):
    # el cero es el format
    profile_picture_name = 'colegiosBanner/media/{0}/banner.png'.format(instance.key_name)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

#Class translate: Colegio
class School(models.Model):
    time_zone = models.CharField(max_length=50, default='UTC')
    photo_cords = models.TextField(null=True, blank=True) #cords
    key_name = models.TextField(max_length=10) #clave
    name = models.TextField(max_length=30) #colegio
    number = models.TextField(max_length=15) #numero
    address = models.TextField(max_length=100) #direccion
    description = models.TextField(max_length=500) #descripcion
    state = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(default='colegiosFoto/profile.png', upload_to=colegio_directory_path_profile, null=True, blank=True) #foto
    banner = models.ImageField(default='colegiosBanner/banner.png', upload_to=colegio_directory_path_banner, null=True, blank=True) #banner

    def __str__(self):
        return self.name
    
    
class CustomUser(AbstractUser):
    time_zone = models.CharField(max_length=50, default='UTC')
    photo_cords = models.TextField(null=True, blank=True) #cords
    document_type = models.CharField(max_length=50,choices=TIPO_DOCUMENTO, default='Sin informacion') # tipo_documento
    document_number = models.CharField(max_length=20, null=True, blank=True) #numero_documento
    introduction = models.TextField(null=True, blank=True) #introduccion
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios') #COLEGIO AL QUE PERTENECE EL USUARIO
    
    def __str__(self):
        return self.username + " defecto"

###########################END CUSTOM USER####################################
def user_directory_path_profile_alumnos(instance, filename):
    # el cero es el format
    profile_picture_name = 'alumnos/media/{0}/profile.png'.format(instance.username)
    #que archivo guardamos..
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    #si el full_path existe lo sacamos y ponemos otro
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

#Class translate: CustomUserAlumno
class CustomUserStudent(CustomUser):
    photo = models.ImageField(default='alumnos/profile.png', upload_to=user_directory_path_profile_alumnos, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Alumno') #tipo_usuario
    creation_date = models.DateTimeField(auto_now_add=True) #fecha_creacion
    grade = models.ForeignKey('informacion.Grade', on_delete=models.SET_NULL, blank=True, null=True)  # Utiliza 'informacion.Grade')  # Campo ForeignKey para relacionar con Grado
    gender = models.CharField(max_length=20, choices=SEXO, default='Sin informacion') # genero
    state = models.BooleanField(default=True) #estado
    #Salud
    description = models.TextField(blank=True, null=True,) # descripcion
    allergies = models.TextField(blank=True, null=True) # alergias
    medical_conditions = models.TextField(blank=True, null=True) #condiciones_medicas
    current_medications = models.TextField(blank=True, null=True) #medicamentos_actuales
    blood_group = models.CharField(max_length=15, blank=True, null=True, choices=TIPO_SANGRE, default='Desconocido') #grupo_sanguineo
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True) #contacto_emergencia_nombre
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True) #contacto_emergencia_telefono
    #pagos
    see_notes = models.BooleanField(default=True) #ver_notas
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - ({self.username}) - {self.user_type}'


###################################################
def user_directory_path_profile_gestor(instance, filename):
    # el cero es el format
    profile_picture_name = 'gestores/media/{0}/profile.png'.format(instance.username)
    #que archivo guardamos..
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    #si el full_path existe lo sacamos y ponemos otro
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

#Class translate: CustomUserGestor
class CustomUserManager(CustomUser):
    photo = models.ImageField(default='gestores/profile.png', upload_to=user_directory_path_profile_gestor, null=True, blank=True) #foto
    user_type = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Gestor') #tipo_usuario
    creation_date = models.DateTimeField(auto_now_add=True) #fecha_creacion
    gender = models.CharField(max_length=20, choices=SEXO, default='Sin informacion') #sexo
    state = models.BooleanField(default=True) #estado

    def __str__(self):
        return self.username + self.user_type

#############################################################

def user_directory_path_profile_profesor(instance, filename):
    # el cero es el format
    profile_picture_name = 'profesores/media/{0}/profile.png'.format(instance.username)
    #que archivo guardamos..
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    #si el full_path existe lo sacamos y ponemos otro
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

#Class translate: CustomUserProfesor
class CustomUserTeachers(CustomUser):
    photo = models.ImageField(default='profesores/profile.png', upload_to=user_directory_path_profile_profesor, null=True, blank=True) #foto
    description = models.TextField(blank=True, null=True) #descripcion
    user_type = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Profesor') #tipo_usuario
    creation_date = models.DateTimeField(auto_now_add=True) #fecha_creacion
    tenured = models.ForeignKey('informacion.Grade', on_delete=models.SET_NULL, blank=True, null=True,related_name='profesor_titulares')  # Utiliza 'informacion.Grade')  # Campo ForeignKey para relacionar con Grado #titular
    gender = models.CharField(max_length=20, choices=SEXO, default='Sin informacion') #sexo
    state = models.BooleanField(default=True) #estado
    #Salud
    allergies = models.TextField(blank=True, null=True) #alergias
    medical_conditions = models.TextField(blank=True, null=True) #condiciones_medicas
    current_medications = models.TextField(blank=True, null=True) #medicamentos_actuales
    blood_group = models.CharField(max_length=15, blank=True, null=True, choices=TIPO_SANGRE, default='Desconocido') #grupo sanguineo
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True) #contacto_emergencia_nombre
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True) #contacto_emergencia_telefono

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ({self.username}) - {self.user_type}'


#######################################################################################################
def user_directory_path_profile_administrador(instance, filename):
    # el cero es el format
    profile_picture_name = 'administradores/media/{0}/profile.png'.format(instance.username)
    #que archivo guardamos..
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    #si el full_path existe lo sacamos y ponemos otro
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

#Class translate: CustomUserAdministrador
class CustomUserAdmin(CustomUser):
    photo = models.ImageField(default='administradores/profile.png', upload_to=user_directory_path_profile_administrador, null=True, blank=True) #foto
    job_title = models.TextField() #cargo
    user_type = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Administrador') #tipo_usuario
    creation_date = models.DateTimeField(auto_now_add=True) #fecha_creacion
    gender = models.CharField(max_length=20, choices=SEXO, default='Sin informacion') #sexo
    state = models.BooleanField(default=True) #estado

    def __str__(self):
        return self.username + self.user_type


###################INICIO PADRES###################
alumno = CustomUserStudent

#Class translate: CustomUserAcudiente
class CustomUserGuardian(CustomUser):
    gender = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    user_type = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Acudiente')
    student = models.ManyToManyField(alumno, blank=True, related_name='estudiantes')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ({self.username}) - {self.user_type}'