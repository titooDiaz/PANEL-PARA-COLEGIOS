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
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Creador_de_materia')
    horas = models.IntegerField(
        default=3,  # Valor predeterminado
        validators=[MinValueValidator(3), MaxValueValidator(12)]
    )

    def __str__(self):
        return "HORARIO DE" + self.titulo
    
class Grado(models.Model):
    grado_nom = models.TextField()
    grado_num = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_grado')
    director = models.ForeignKey(UserProfes, on_delete=models.SET_NULL, blank=True, null=True, related_name='grado_director')
    alumnos = models.ManyToManyField(UserAlumno, blank=True, related_name='grado_alumnos')
    materias = models.ManyToManyField('Materias', blank=True, related_name='grados_relacionados')
    horario = models.ManyToManyField('Materias', blank=True, related_name='horario_establecido')

    def __str__(self):
        return self.grado_nom + "(" + self.grado_num + ")"

class Materias(models.Model):
    titulo = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_materia')
    profes = models.ManyToManyField(UserProfes, blank=True, related_name='materias_relacionadas')

    def __str__(self):
        return self.titulo

