from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUserProfesores
from users.models import CustomUserAlumno

from django.contrib.auth import get_user_model
User = get_user_model()
UserProfes = CustomUserProfesores
UserAlumno = CustomUserAlumno
    
class Colegio(models.Model):
    colegio_nom = models.TextField()
    numero = models.TextField()
    direccion = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_colegio')

    def __str__(self):
        return self.colegio_nom

class Horarios_Partes(models.Model):
    titulo = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_de_materia')
    horas = models.IntegerField(
        default=3,
        validators=[MinValueValidator(3), MaxValueValidator(22)]
    )

    def __str__(self):
        return "HORARIO DE " + self.titulo

class Materias(models.Model):
    electiva = models.BooleanField(default=True)
    ##################electivas##############
    profe1 = models.ForeignKey(UserProfes,on_delete=models.CASCADE, blank=True, related_name='profesor_0')
    titulo1 = models.TextField(blank=True, null=True)
    descripcion1 = models.TextField(blank=True, null=True)
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
    grado_nom = models.TextField()
    grado_num = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_grado')
    horario_partes = models.ForeignKey(Horarios_Partes, on_delete=models.SET_NULL, blank=True, null=True)
    materias = models.ManyToManyField(Materias, blank=True, related_name='materias_grado')

    def __str__(self):
        return self.grado_nom + "(" + self.grado_num + ")"

class HorarioDiario(models.Model): #Materias por dia (DEPENDIENDO DEL HORARIO SE VA A ITERAR SOBRE ESTE MODELO PARA CREAR LAS CLASES DIARIAS NECESARIAS)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    """LOS MODELOS TIENEN NOMBRES DE DIAS PERO REALMENTE SE REFIEREN A LAS MATERIAS DE ESTE DIA
         |
        \|/                                                                               """
    lunes = models.ForeignKey(Materias, on_delete=models.CASCADE, blank=True, null=True, related_name='materias_grado_1')
    martes = models.ForeignKey(Materias, on_delete=models.CASCADE, blank=True, null=True, related_name='materias_grado_2')
    miercoles = models.ForeignKey(Materias, on_delete=models.CASCADE, blank=True, null=True, related_name='materias_grado_3')
    jueves = models.ForeignKey(Materias, on_delete=models.CASCADE, blank=True, null=True, related_name='materias_grado_4')
    viernes = models.ForeignKey(Materias, on_delete=models.CASCADE, blank=True, null=True, related_name='materias_grado_5')

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"

    

