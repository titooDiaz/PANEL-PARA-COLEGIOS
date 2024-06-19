from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUserAlumno, CustomUserProfesores, Colegio

from django.contrib.auth import get_user_model
User = get_user_model()
UserProfes = CustomUserProfesores
UserAlumno = CustomUserAlumno

def ano_actual():
    ano_electivo = timezone.now().year
    ano_electivo = int(ano_electivo)
    return ano_electivo

class Anos_electivos(models.Model):
    ano = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_Ano_electivo')
    estado = models.BooleanField(default=True)
    
class Horarios_Partes(models.Model):
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE, null=True, blank=True, related_name='ColegioHorariosPartes') #COLEGIO AL QUE PERTENECE EL USUARIO
    titulo = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_de_materia')
    ano_creacion = models.IntegerField(default=ano_actual())
    horas = models.IntegerField(
        default=3,
        validators=[MinValueValidator(3), MaxValueValidator(22)]
    )
    cortes = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )

    def __str__(self):
        return "HORARIO DE " + self.titulo

class Materias(models.Model):
    electiva = models.BooleanField(default=False)
    ano_creacion = models.IntegerField(default=ano_actual())
    ##################electivas##############
    profe1 = models.ForeignKey(UserProfes,on_delete=models.CASCADE, blank=True, related_name='profesor_0')
    titulo1 = models.TextField(blank=True, null=False)
    descripcion1 = models.TextField(blank=True, null=False)
    alumnos1 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva1')

    profe2 = models.ForeignKey(UserProfes,on_delete=models.CASCADE, blank=True, null=True, related_name='profesor_1')
    titulo2 = models.TextField(blank=True, null=True)
    descripcion2 = models.TextField(blank=True, null=True)
    alumnos2 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva2')
    ##########################################
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_materia')

    def __str__(self):
        return f'{self.titulo1} - {self.profe1}'

class Grado(models.Model):
    ano_creacion = models.IntegerField(default=ano_actual())
    grado_nom = models.TextField()
    grado_num = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_grado')
    horario_partes = models.ForeignKey(Horarios_Partes, on_delete=models.SET_NULL, blank=True, null=True)
    materias = models.ManyToManyField(Materias, blank=True, related_name='materias_grado')
    colegio = models.ForeignKey(Colegio, on_delete=models.CASCADE, null=True, blank=True, related_name='ColegioGrado') #COLEGIO AL QUE PERTENECE EL USUARIO

    def __str__(self):
        return self.grado_nom + "(" + self.grado_num + ")"

class HorarioDiario(models.Model): #Materias por dia (DEPENDIENDO DEL HORARIO SE VA A ITERAR SOBRE ESTE MODELO PARA CREAR LAS CLASES DIARIAS NECESARIAS)
    ano_creacion = models.IntegerField(default=ano_actual())
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    """LOS MODELOS TIENEN NOMBRES DE DIAS PERO REALMENTE SE REFIEREN A LAS MATERIAS DE ESTE DIA
         |
        \|/                                                                               """
    lunes = models.ForeignKey(Materias, on_delete=models.SET_NULL, blank=True, null=True, related_name='materias_grado_1')
    martes = models.ForeignKey(Materias, on_delete=models.SET_NULL, blank=True, null=True, related_name='materias_grado_2')
    miercoles = models.ForeignKey(Materias, on_delete=models.SET_NULL, blank=True, null=True, related_name='materias_grado_3')
    jueves = models.ForeignKey(Materias, on_delete=models.SET_NULL, blank=True, null=True, related_name='materias_grado_4')
    viernes = models.ForeignKey(Materias, on_delete=models.SET_NULL, blank=True, null=True, related_name='materias_grado_5')

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"
    
class CortesHorario(models.Model): #Materias por dia (DEPENDIENDO DEL HORARIO SE VA A ITERAR SOBRE ESTE MODELO PARA CREAR LAS CLASES DIARIAS NECESARIAS)
    ano_creacion = models.IntegerField(default=ano_actual())
    corte_num = models.IntegerField(blank=False)
    horario = models.ForeignKey(Horarios_Partes, on_delete=models.CASCADE)
    fecha_inicio = models.TimeField(blank=True, null=True)
    fecha_fin = models.TimeField(blank=True, null=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.horario.titulo} - CORTE {self.corte_num}"