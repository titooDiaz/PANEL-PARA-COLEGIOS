from django.contrib import admin
from .models import CustomUserAlumno, CustomUserAdministrador, CustomUserGestor, CustomUserProfesores

class CustomUserAlumnoProxy(CustomUserAlumno):
    class Meta:
        proxy = True
        #verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

class CustomUserAdministradorProxy(CustomUserAdministrador):
    class Meta:
        proxy = True
        #verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

class CustomUserGestorProxy(CustomUserGestor):
    class Meta:
        proxy = True
        #verbose_name = 'Gestor'
        verbose_name_plural = 'Gestores'

class CustomUserProfesoresProxy(CustomUserProfesores):
    class Meta:
        proxy = True
        #verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'


admin.site.register(CustomUserAlumnoProxy)
admin.site.register(CustomUserAdministradorProxy)
admin.site.register(CustomUserGestorProxy)
admin.site.register(CustomUserProfesoresProxy)
