from django.contrib.auth.models import AbstractUser
from django.conf import settings # usar los settings
from django.db import models
import os

def user_directory_path_profile(instance, filename):
    # el cero es el format
    profile_picture_name = 'alumnos/{0}/profile.jpg'.format(instance.user.username)
    #que archivo guardamos..
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    #si el full_path existe lo sacamos y ponemos otro
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


SEXO = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Sin informacion', 'Sin informacion'),
    ]
class CustomUserAlumno(AbstractUser):
    picture = models.ImageField(default='alumnos/user_default_profile.png', upload_to=user_directory_path_profile, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tipo_documento = models.CharField(max_length=50, null=True, blank=True)
    numero_documento = models.CharField(max_length=20, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=50,default='Alumno')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    #grado = models.IntegerField(null=True, blank=True)
    #curso = models.CharField(max_length=10, null=True, blank=True)
    sexo = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    estdo = models.BooleanField(default=True)

    def __str__(self):
        return self.username


def user_directory_path_profile(instance, filename):
    # el cero es el format
    profile_picture_name = 'alumnos/{0}/profile.jpg'.format(instance.user.username)
    #que archivo guardamos..
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    #si el full_path existe lo sacamos y ponemos otro
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name
