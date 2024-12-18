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

TIPO_RESTRICCION = [
        ('0', 'NO VERAN MAS LA ACTIVIDAD'),
        ('1', 'PUEDEN SUBIR LA ACTIVIDAD PERO CON ADVERTENCIA'),
]


def ano_actual():
    ano_electivo = timezone.now().year
    ano_electivo = int(ano_electivo)
    return ano_electivo

# Translate class: Anos_Electivos
class ElectiveYears(models.Model):
    year = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Creator_Elective_Year')
    state = models.BooleanField(default=True)

# Translate class: Horarios_Partes
class ScheduleParts(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='ColegioHorariosPartes') #COLEGIO AL QUE PERTENECE EL USUARIO #colegio
    name = models.TextField() #titulo
    description = models.TextField() #descipcion
    state = models.BooleanField(default=True) #estado
    created_on = models.DateTimeField(auto_now_add=True) #create_on
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_de_materia') # author
    year_creation = models.IntegerField(default=ano_actual()) #ano_creacion
    hours = models.IntegerField(
        default=3,
        validators=[MinValueValidator(3), MaxValueValidator(22)]
    ) #horas
    school_cuts = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    ) #cortes

    def __str__(self):
        return "HORARIO DE " + self.name

def picture_materia_1(instance, filename):
    profile_picture_name = 'materias/media/{0}/{1}/{2}/picture.png'.format(instance.name_1, instance.teacher_1, random.randint(1, 9999))
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_picture_name


# Translate class: Materias
class Subjects(models.Model):   
    elective = models.BooleanField(default=False) #electiva
    year_creation = models.IntegerField(default=ano_actual()) #ano_creacion
    ##################electivas##############
    photo = models.ImageField(default='materias/picture.png', upload_to=picture_materia_1, null=True, blank=True) #picture1
    cords = models.TextField(blank=True, null=False) #cords
    teacher_1 = models.ForeignKey(UserProfes,on_delete=models.CASCADE, blank=True, related_name='profesor_0') #profe1
    name_1 = models.TextField(blank=True, null=False) #titulo1
    description_1 = models.TextField(blank=True, null=False) #descripcion1
    location_1 = models.TextField(blank=True, null=False) #locate1
    students_1 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva1') #alumnos1

    teacher_2 = models.ForeignKey(UserProfes,on_delete=models.CASCADE, blank=True, null=True, related_name='profesor_1') #profe2
    name_2 = models.TextField(blank=True, null=True) #titulo2
    location_2 = models.TextField(blank=True, null=False) #locate2
    description_2 = models.TextField(blank=True, null=True) #descripcion2
    students_2 = models.ManyToManyField(UserAlumno, blank=True, related_name='alumnos_electiva2') #alumnos2
    ##########################################
    state = models.BooleanField(default=True) #estado
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_materia')

    def __str__(self):
        return f'{self.name_1}'

# Translate class: Grado 
class Grade(models.Model):
    year_creation = models.IntegerField(default=ano_actual()) #ano_creacion
    grade_name = models.TextField() #grado_nom
    grade_number = models.TextField() #grado_num
    description = models.TextField() #descripcion
    state = models.BooleanField(default=True) #estado
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_grado')
    schedule_parts = models.ForeignKey(ScheduleParts, on_delete=models.SET_NULL, blank=True, null=True) #horario_partes
    subjects = models.ManyToManyField(Subjects, blank=True, related_name='materias_grado') #materias
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='ColegioGrado') #COLEGIO AL QUE PERTENECE EL USUARIO #colegio

    def __str__(self):
        return self.grade_name + "(" + self.grade_number + ")"

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
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadesColegio') #COLEGIO AL QUE PERTENECE EL USUARIO #colegio
    name = models.TextField(null=False, blank=False) #titulo
    description = models.TextField(null=False, blank=False) #description
    state = models.BooleanField(default=True) #estado
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_de_tipo_actividad')
    year_creation = models.IntegerField(default=ano_actual()) #ano_creacion
    
    def __str__(self):
        return f"Actividad: {self.name}"


# Translate class: Actividades
class Activities(models.Model):
    name = models.TextField() #titulo
    description = models.TextField() #descripcion
    percentage = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)]) #porcentaje
    type = models.ForeignKey(ActivitiesType, on_delete=models.CASCADE, related_name='actividades') #tipo
    restriction = models.CharField(max_length=50, choices=TIPO_RESTRICCION, default=None) #restriccion
    start_date = models.DateField(default=get_current_date) #fecha_inicio
    end_date = models.DateField(default=get_current_date) #fecha_final
    start_time = models.TimeField(default=get_current_time) #hora_inicio
    end_time = models.TimeField(default=get_current_time) #hora_final
    location_time_zone= models.TextField(null=True) #lugar_zona_horaria
    time_zone = models.BooleanField(default=True) # cuando este activa significa que sera en el lugar que se encuntre el profesor en este momento #zona_horaria
    #si esta inactiva significa que se colocara la fecha donde se creo su perfil!
    #esta opcion solo aprece cuando los lugares y la zona horario es diferente
    
    year_creation = models.IntegerField(default=ano_actual()) #ano_creacion
    state = models.BooleanField(default=True) #estado
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_actividad')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadMateria') #materia

    def __str__(self):
        return f"{self.name} ({self.pk})"


def files(instance, filename):
    archivo_guia = 'actividades_profesores/media/grado{0}({1})/{2}'.format(
        instance.actividad.titulo, instance.actividad.pk, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, archivo_guia)
    if os.path.exists(full_path):
        os.remove(full_path)
    return archivo_guia

# Translate class: Archivo
class File(models.Model):
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name='archivos') #actividad
    file = models.FileField(upload_to=files) #archivo
    name = models.CharField(max_length=40, blank=True) #nombre
    description = models.CharField(max_length=255, blank=True) #descripcion

    def __str__(self):
        return self.name or self.file.name


def files_respuesta(instance, filename):
    archivo_respuesta = 'respuesta_estudiantes_actividades/{0}/{1}'.format(
        instance.actividad_respuesta.actividad, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, archivo_respuesta)
    if os.path.exists(full_path):
        os.remove(full_path)
    return archivo_respuesta


# Translate class: Actividades_Respuesta_Estudiantes
class StudentResponse(models.Model):
    answer = models.TextField() #respuesta
    description = models.TextField() #descripcion
    delivery_date = models.DateField(default=get_current_date) #fecha_entrega
    delivery_time = models.TimeField(default=get_current_time) #hora_entrega
    timezone_response = models.TextField(null=True) #lugar_zona_horaria
    same_zone = models.BooleanField(default=True) # Si el estudiante cambia la fecha, este elemento saldrá como falso #misma_zona
    year_creation = models.IntegerField(default=ano_actual) #ano_creacion
    state = models.BooleanField(default=True) #estado
    created_on = models.DateTimeField(default=timezone.now) #create_on
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creador_respuesta')
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, null=True, blank=True, related_name='ActividadRespuesta') #actividad

    def __str__(self):
        return f"ACTIVIDAD ENTREGADA POR: {self.author}"

# Translate class: ArchivoEstudiantes
class StudentFiles(models.Model):
    activity_answer = models.ForeignKey(StudentResponse, on_delete=models.CASCADE, related_name='archivos') #actividad_respuesta
    file = models.FileField(upload_to=files_respuesta) #archivo

    def __str__(self):
        return f"Archivo para {self.activity_answer.author}: {self.file}"

# Translate class: HorarioDiario
class DailySchedule(models.Model): #Materias por dia (DEPENDIENDO DEL HORARIO SE VA A ITERAR SOBRE ESTE MODELO PARA CREAR LAS CLASES DIARIAS NECESARIAS)
    year_creation = models.IntegerField(default=ano_actual()) #ano_creacion
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE) #grado
    start_time = models.TimeField(blank=True, null=True) #hora_inicio
    end_time = models.TimeField(blank=True, null=True) #hora_fin
    """LOS MODELOS TIENEN NOMBRES DE DIAS PERO REALMENTE SE REFIEREN A LAS MATERIAS DE ESTE DIA
         |
        \|/                                                                               """
    monday = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_1')#lunes
    tuesday = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_2') #martes
    wednesday= models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_3') #miercoles
    thursday = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_4') #jueves 
    friday = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_5') #viernes
    saturday = models.ForeignKey(Subjects, on_delete=models.SET_NULL, blank=True, null=True, related_name='subjects_grade_5') #viernes

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


# Translate class: HorarioCortes
class ScheduleCourts(models.Model): 
    year_creation = models.IntegerField(default=ano_actual()) #ano_creacion
    schedule = models.ForeignKey(ScheduleParts, on_delete=models.CASCADE) #horario
    start_date = models.DateField(blank=True, null=True) #fecha_inicio
    end_date = models.DateField(blank=True, null=True) #fecha_fin
    court_number = models.IntegerField(blank=False) #corte_num
    file = models.BooleanField(default=False) #archivo
    
    def __str__(self):
        return f"{self.start_date} - {self.end_date}"