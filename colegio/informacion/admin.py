from django.contrib import admin
from .models import Horarios_Partes, Grado, Materias


class Horarios_PartesProxy(Horarios_Partes):
    class Meta:
        proxy = True
        verbose_name_plural = 'Fraccion de horarios'

class MateriasProxy(Materias):
    class Meta:
        proxy = True
        verbose_name_plural = 'Materias Escolares'

class GradoProxy(Grado):
    class Meta:
        proxy = True
        verbose_name_plural = 'Grados Escolares'


admin.site.register(Horarios_PartesProxy)
admin.site.register(GradoProxy)
admin.site.register(MateriasProxy)