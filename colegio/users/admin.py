from django.contrib import admin
from .models import CustomUserStudent, CustomUserAdmin, CustomUserManager, CustomUserTeachers, CustomUserGuardian, CustomUser, School

class CustomUserStudentProxy(CustomUserStudent):
    class Meta:
        proxy = True
        verbose_name_plural = 'Alumnos'

class CustomUserAdminProxy(CustomUserAdmin):
    class Meta:
        proxy = True
        verbose_name_plural = 'Administradores'

class CustomUserManagerProxy(CustomUserManager):
    class Meta:
        proxy = True
        verbose_name_plural = 'Gestores'

class CustomUserTeachersProxy(CustomUserTeachers):
    class Meta:
        proxy = True
        verbose_name_plural = 'Profesores'

class CustomUserGuardianProxy(CustomUserGuardian):
    class Meta:
        proxy = True
        verbose_name_plural = 'Acudiente'

class CustomUserProxy(CustomUser):
    class Meta:
        proxy = True
        verbose_name_plural = 'General'
class SchoolProxy(School):
    class Meta:
        proxy = True
        verbose_name_plural = 'Schools'

admin.site.register(CustomUser)
admin.site.register(CustomUserStudentProxy)
admin.site.register(CustomUserGuardianProxy)
admin.site.register(CustomUserAdminProxy)
admin.site.register(CustomUserManagerProxy)
admin.site.register(CustomUserTeachersProxy)
admin.site.register(School)
