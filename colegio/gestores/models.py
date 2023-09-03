from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings # usar los settings
from django.db import models
import os

def user_directory_path_profile(instance, filename):
    # el cero es el format
    profile_picture_name = 'gestores/{0}/profile.png'.format(instance.username)
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
TIPO_USUARIO = [
        ('Profesor', 'Profesor'),
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
class CustomUserGestor(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='gestor_user_set',  # Cambia esto a tu preferencia
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='gestor_user_set',  # Cambia esto a tu preferencia
    )
    foto = models.ImageField(default='gestores/profile.png', upload_to=user_directory_path_profile, null=True, blank=True)
    tipo_documento = models.CharField(max_length=50,choices=TIPO_DOCUMENTO, default='Sin informacion')
    numero_documento = models.CharField(max_length=20, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO, default='Gestor')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    sexo = models.CharField(max_length=20, choices=SEXO, default='Sin informacion')
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.username + self.tipo_usuario


def user_directory_path_profile(instance, filename):
    # el cero es el format
    profile_picture_name = 'gestores/{0}/profile.jpg'.format(instance.user.username)
    #que archivo guardamos..
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    #si el full_path existe lo sacamos y ponemos otro
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name