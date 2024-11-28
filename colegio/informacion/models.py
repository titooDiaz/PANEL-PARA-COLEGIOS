from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUserStudent, CustomUserTeachers, School
from django.conf import settings
import os
import random

from django.contrib.auth import get_user_model
User = get_user_model()
UserProfes = CustomUserTeachers
UserAlumno = CustomUserStudent


TIPO_ACTIVIDAD = [
        ('EVALUATIVA', 'EVALUATIVA'),
        ('ASIMILATIVA', 'ASIMILATIVA'),
        ('EXPERIENCIAL', 'EXPERIENCIAL'),
        ('GESTION DE INFORMACION', 'GESTION DE INFORMACION'),
        ('APLICACION', 'APLICACION'),
        ('COMUNICATIVA', 'COMUNICATIVA'),
        ('PRODUCTIVA', 'PRODUCTIVA')
]

tipo_de_restriccion = 'NO VERAN MAS LA ACTIVIDAD'
TIPO_RESTRICCION = [
        (tipo_de_restriccion, '0'),
        ('PUEDEN SUBIR LA ACTIVIDAD PERO CON ADVERTENCIA', '1'),
]


def ano_actual():
    ano_electivo = timezone.now().year
    ano_electivo = int(ano_electivo)
    return ano_electivo

# Translate class: Anos_Electivos
class ElectiveYears(models.Model):
    ano = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Creator_Elective_Year')
    estado = models.BooleanField(default=True)

# Translate class: Horarios_Partes
class ScheduleParts(models.Model):
    colegio = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='ColegioHorariosPartes') #COLEGIO AL QUE PERTENECE EL USUARIO
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

def picture_materia_1(instance, filename):
    profile_picture_name = 'materias/media/{0}/{1}/{2}/picture.png'.format(instance.titulo1, instance.profe1, random.randint(1, 9999))
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_picture_name


# Translate class: Materias
class Subjects(models.Model):   
    electiva = models.BooleanField(default=False)
    ano_creacion = models.IntegerField(default=ano_actual())
    ##################electivas##############
    picture1 = models.ImageField(default='materias/picture.png', upload_to=picture_materia_1, null=True, blank=True)
    cords = models.TextField(blank=True, null=False)
    profe1 = models.ForeignKey(UserProfes,on_delete=models.CASCADE, blank=True, related_name='profesor_0')
    titulo1 = models.TextField(blank=True, null=False)
    descripcion1 = models.TextField(blank=True, null=False)
    locate1 = models.TextField(blank=True, null=False)
    alumnos1 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva1')

    profe2 = models.ForeignKey(UserProfes,on_delete=models.CASCADE, blank=True, null=True, related_name='profesor_1')
    titulo2 = models.TextField(blank=True, null=True)
    locate2 = models.TextField(blank=True, null=False)
    descripcion2 = models.TextField(blank=True, null=True)
    alumnos2 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva2')
    ##########################################
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_materia')

    def __str__(self):
        return f'{self.titulo1}'

# Translate class: Grado 
class Grade(models.Model):
    ano_creacion = models.IntegerField(default=ano_actual())
    grado_nom = models.TextField()
    grado_num = models.TextField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_grado')
    horario_partes = models.ForeignKey(ScheduleParts, on_delete=models.SET_NULL, blank=True, null=True)
    materias = models.ManyToManyField(Subjects, blank=True, related_name='materias_grado')
    colegio = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='ColegioGrado') #COLEGIO AL QUE PERTENECE EL USUARIO

    def __str__(self):
        return self.grado_nom + "(" + self.grado_num + ")"

def get_current_date():
    fecha_actual = timezone.now().date()
    # Convertir la fecha a una cadena en el formato 'YYYY-MM-DD'
    fecha_actual_formateada = fecha_actual.strftime('%Y-%m-%d')

    return fecha_actual_formateada

def get_current_time():
    now = timezone.now()
    return now.replace(second=0, microsecond=0).time()


# Translate class: ActividadesTipo
class ActivitiesType(models.Model):
    colegio = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadesColegio') #COLEGIO AL QUE PERTENECE EL USUARIO
    titulo = models.TextField(null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False)
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_de_tipo_actividad')
    ano_creacion = models.IntegerField(default=ano_actual())
    
    def __str__(self):
        return f"Actividad: {self.titulo}"


# Translate class: Actividades
class Activities(models.Model):
    titulo = models.TextField()
    descripcion = models.TextField()
    porcentaje = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    tipo = models.ForeignKey(ActivitiesType, on_delete=models.CASCADE, related_name='actividades')
    restriccion = models.CharField(max_length=50, choices=TIPO_RESTRICCION, default=tipo_de_restriccion)
    fecha_inicio = models.DateField(default=get_current_date)
    fecha_final = models.DateField(default=get_current_date)
    hora_inicio = models.TimeField(default=get_current_time)
    hora_final = models.TimeField(default=get_current_time)
    lugar_zona_horaria = models.TextField(null=True)
    zona_horaria = models.BooleanField(default=True) # cuando este activa significa que sera en el lugar que se encuntre el profesor en este momento
    #si esta inactiva significa que se colocara la fecha donde se creo su perfil!
    #esta opcion solo aprece cuando los lugares y la zona horario es diferente
    
    ano_creacion = models.IntegerField(default=ano_actual())
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_actividad')
    materia = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadMateria')

    def __str__(self):
        return f"{self.titulo} ({self.pk})"


def files(instance, filename):
    archivo_guia = 'actividades_profesores/media/grado{0}({1})/{2}'.format(
        instance.actividad.titulo, instance.actividad.pk, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, archivo_guia)
    if os.path.exists(full_path):
        os.remove(full_path)
    return archivo_guia

# Translate class: Archivo
class File(models.Model):
    actividad = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to=files)
    nombre = models.CharField(max_length=40, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre or self.archivo.name


def files_respuesta(instance, filename):
    archivo_respuesta = 'respuesta_estudiantes_actividades/{0}/{1}'.format(
        instance.actividad_respuesta.actividad, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, archivo_respuesta)
    if os.path.exists(full_path):
        os.remove(full_path)
    return archivo_respuesta


# Translate class: Actividades_Respuesta_Estudiantes
class StudentResponse(models.Model):
    respuesta = models.TextField()
    descripcion = models.TextField()
    fecha_entrega = models.DateField(default=get_current_date)
    hora_entrega = models.TimeField(default=get_current_time)
    lugar_zona_horaria = models.TextField(null=True)
    misma_zona = models.BooleanField(default=True) # Si el estudiante cambia la fecha, este elemento saldrá como falso
    ano_creacion = models.IntegerField(default=ano_actual)
    estado = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_respuesta')
    actividad = models.ForeignKey(Activities, on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadRespuesta')

    def __str__(self):
        return f"ACTIVIDAD ENTREGADA POR: {self.author}"

# Translate class: ArchivoEstudiantes
class StudentFiles(models.Model):
    actividad_respuesta = models.ForeignKey(StudentResponse, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to=files_respuesta)

    def __str__(self):
        return f"Archivo para {self.actividad_respuesta.author}: {self.archivo.name}"

# Translate class: HorarioDiario
class DailySchedule(models.Model): #Materias por dia (DEPENDIENDO DEL HORARIO SE VA A ITERAR SOBRE ESTE MODELO PARA CREAR LAS CLASES DIARIAS NECESARIAS)
    ano_creacion = models.IntegerField(default=ano_actual())
    grado = models.ForeignKey(Grade, on_delete=models.CASCADE)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    """LOS MODELOS TIENEN NOMBRES DE DIAS PERO REALMENTE SE REFIEREN A LAS MATERIAS DE ESTE DIA
         |
        \|/                                                                               """
    lunes = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_1')
    martes = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_2')
    miercoles = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_3')
    jueves = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_4')
    viernes = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_5')

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"


# Translate class: HorarioCortes
class ScheduleCourts(models.Model): 
    ano_creacion = models.IntegerField(default=ano_actual())
    horario = models.ForeignKey(ScheduleParts, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    corte_num = models.IntegerField(blank=False)
    activo = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.fecha_inicio} - {self.fecha_fin}"