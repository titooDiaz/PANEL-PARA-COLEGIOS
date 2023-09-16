from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUserProfesores
from users.models import CustomUserAlumno

from django.contrib.auth import get_user_model
User = get_user_model()
UserProfes = CustomUserProfesores
UserAlumno = CustomUserAlumno
    
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
    

class HorarioDiario(models.Model):
    Hora = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.dia}"


class Materias(models.Model):
    ##################electivas##############
    profe = models.ManyToManyField(UserProfes, blank=True, related_name='materias_grado')
    electiva = models.BooleanField(default=True)
    titulo1 = models.TextField(blank=True, null=True)
    descripcion1 = models.TextField(blank=True, null=True)
    alumnos1 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva1')

    titulo2 = models.TextField(blank=True, null=True)
    descripcion2 = models.TextField(blank=True, null=True)
    alumnos2 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva2')
    ##########################################
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_materia')

    def __str__(self):
        return f'{self.titulo} - {self.profe}'
    
class Grado(models.Model):
    grado_nom = models.TextField()
    grado_num = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_grado')
    director = models.ForeignKey(UserProfes, on_delete=models.SET_NULL, blank=True, null=True, related_name='grado_director')
    alumnos = models.ManyToManyField(UserAlumno, blank=True, related_name='grado_alumnos')
    horario_partes = models.ForeignKey(Horarios_Partes, on_delete=models.SET_NULL, blank=True, null=True)
    horario = models.ForeignKey(HorarioDiario, on_delete=models.SET_NULL, blank=True, null=True)
    materias = models.ManyToManyField(Materias, blank=True, related_name='materias_grado')

    def __str__(self):
        return self.grado_nom + "(" + self.grado_num + ")"