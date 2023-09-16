from django.contrib import admin
from .models import Horarios_Partes, Grado, Materias, HorarioDiario


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

class HorarioDiarioProxy(HorarioDiario):
    class Meta:
        proxy = True
        verbose_name_plural = 'Horarios Escolares'

admin.site.register(HorarioDiarioProxy)
admin.site.register(Horarios_PartesProxy)
admin.site.register(GradoProxy)
admin.site.register(MateriasProxy)