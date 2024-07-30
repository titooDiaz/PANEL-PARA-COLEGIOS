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
    profile_picture_name = 'colegiosFoto/{0}/profile.png'.format(instance.clave)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

def colegio_directory_path_banner(instance, filename):
    # el cero es el format
    profile_picture_name = 'colegiosBanner/media/{0}/banner.png'.format(instance.clave)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name
class Colegio(models.Model):
    time_zone = models.CharField(max_length=50, default='UTC')
    cords = models.TextField(null=True, blank=True)
    clave = models.TextField(max_length=10)
    colegio = models.TextField(max_length=30)
    numero = models.TextField(max_length=15)
    direccion = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=500)
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    foto = models.ImageField(default='colegiosFoto/profile.png', upload_to=colegio_directory_path_profile, null=True, blank=True)
    banner = models.ImageField(default='colegiosBanner/banner.png', upload_to=colegio_directory_path_banner, null=True, blank=True)

    def __str__(self):
        return self.colegio
    
    
class CustomUser(AbstractUser):
    time_zone = models.CharField(max_length=50, default='UTC')
    cords = models.TextField(null=True, blank=True)
    tipo_documento = models.CharField(max_length=50,choices=TIPO_DOCUMENTO, default='Sin informacion')
    numero_documento = models.CharField(max_length=20, null=True, blank=True)
    introduccion = models.TextField(null=True, blank=True)
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios') #COLEGIO AL QUE PERTENECE EL USUARIO
    
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


class CustomUserAlumno(CustomUser):
    foto = models.ImageField(default='alumnos/profile.png', upload_to=user_directory_path_profile_alumnos, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Alumno')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    grado = models.ForeignKey('informacion.Grado', on_delete=models.SET_NULL, blank=True, null=True)  # Utiliza 'informacion.Grado')  # Campo ForeignKey para relacionar con Grado
    sexo = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    estado = models.BooleanField(default=True)
    #Salud
    descripcion = models.TextField(blank=True, null=True,)
    alergias = models.TextField(blank=True, null=True)
    condiciones_medicas = models.TextField(blank=True, null=True)
    medicamentos_actuales = models.TextField(blank=True, null=True)
    grupo_sanguineo = models.CharField(max_length=15, blank=True, null=True, choices=TIPO_SANGRE, default='Desconocido')
    contacto_emergencia_nombre = models.CharField(max_length=255, blank=True, null=True)
    contacto_emergencia_telefono = models.CharField(max_length=20, blank=True, null=True)
    #pagos
    ver_notas = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - ({self.username}) - {self.tipo_usuario}'


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
class CustomUserGestor(CustomUser):
    foto = models.ImageField(default='gestores/profile.png', upload_to=user_directory_path_profile_gestor, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Gestor')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    sexo = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.username + self.tipo_usuario

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

class CustomUserProfesores(CustomUser):
    foto = models.ImageField(default='profesores/profile.png', upload_to=user_directory_path_profile_profesor, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Profesor')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    titular = models.ForeignKey('informacion.Grado', on_delete=models.SET_NULL, blank=True, null=True,related_name='profesor_titulares')  # Utiliza 'informacion.Grado')  # Campo ForeignKey para relacionar con Grado
    sexo = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    estado = models.BooleanField(default=True)
    #Salud
    alergias = models.TextField(blank=True, null=True)
    condiciones_medicas = models.TextField(blank=True, null=True)
    medicamentos_actuales = models.TextField(blank=True, null=True)
    grupo_sanguineo = models.CharField(max_length=15, blank=True, null=True, choices=TIPO_SANGRE, default='Desconocido')
    contacto_emergencia_nombre = models.CharField(max_length=255, blank=True, null=True)
    contacto_emergencia_telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ({self.username}) - {self.tipo_usuario}'


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

class CustomUserAdministrador(CustomUser):
    foto = models.ImageField(default='administradores/profile.png', upload_to=user_directory_path_profile_administrador, null=True, blank=True)
    cargo = models.TextField()
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Administrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    sexo = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.username + self.tipo_usuario


###################INICIO PADRES###################
alumno = CustomUserAlumno
class CustomUserAcudiente(CustomUser):
    sexo = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Acudiente')
    estudiante = models.ManyToManyField(alumno, blank=True, related_name='estudiantes')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ({self.username}) - {self.tipo_usuario}'