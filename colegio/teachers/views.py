from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from information.models import Subjects, Grade, Activities, File, ActivitiesType, StudentResponse, DailySchedule, Rating
from .forms import ActivitiesForm, FileForm, FilesProfesoresForm, RatingForm
from django.contrib import messages
## MENSAJES DE ERRORES ##
from message_error import messages_error
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist
from itertools import groupby
from operator import attrgetter
from django.shortcuts import get_object_or_404
from django.db import transaction
from users.models import CustomUser, CustomUserStudent

# in real time
from django.http import JsonResponse

# maage directories
import os

#
from django.contrib.auth import get_user_model
from users.models import CustomUserTeachers, CustomUserStudent
UserProfes = CustomUserTeachers
UserAlumno = CustomUserStudent

## Contar, Agrupar, un modelo
from itertools import groupby
from operator import attrgetter
from django.db.models import Count
from collections import defaultdict

# LIBRERIAS DE FECHAS
from datetime import datetime
import pytz
import time
import tzlocal #pip install tzlocal

# time now!
from utils.functions import time_zone_user_location

class BoardTeachers(View):
    def get(self, request, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        profesor = request.user.pk
        materias_profesor = Subjects.objects.filter(teacher_1_id=profesor) | Subjects.objects.filter(teacher_2_id=profesor)
        grades = Grade.objects.filter(subjects__in=materias_profesor).distinct()
        actividades = Activities.objects.filter(subject__in=materias_profesor)

        #Time zone
        DateNow, TimeNow = time_zone_user_location(request.user.time_zone)
            
        context = {
            'grades': grades,
            'materias_profesor': materias_profesor,
            'vista': vista,
            'abierto':abierto,
            'actividades': actividades,
            'hora_actual': TimeNow,
            'fecha_actual': DateNow,
        }
        return render(request, 'users/teachers/inicio.html', context)


import pytz
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def get_user_timezone(user):
    return user.time_zone

def get_current_date(user):
    user_timezone_str = get_user_timezone(user)
    user_timezone = pytz.timezone(user_timezone_str)
    fecha_actual = timezone.now().astimezone(user_timezone).date()
    return fecha_actual.strftime('%Y-%m-%d')

def get_current_time(user):
    user_timezone_str = get_user_timezone(user)
    user_timezone = pytz.timezone(user_timezone_str)
    now = timezone.now().astimezone(user_timezone)
    return now.replace(second=0, microsecond=0).time()

def get_midnight(user):
    user_timezone_str = get_user_timezone(user)
    user_timezone = pytz.timezone(user_timezone_str)
    now = timezone.now().astimezone(user_timezone)
    # Ajusta la hora a las 12 de la noche (medianoche) en la zona horaria del usuario
    midnight_user_tz = now.replace(hour=23, minute=59, second=0, microsecond=0)
    return midnight_user_tz



class CreateActividades(View):
    def get(self, request, pk, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        materia = Subjects.objects.get(pk=pk)
        author = request.user
        grade = Grade.objects.filter(subjects=materia).first()
        tipo_actividades = ActivitiesType.objects.filter(school_id=request.user.school)
        
        activities = Activities.objects.filter(author=author,subject=materia).values_list('percentage', flat=True)
        total_percentage = sum(activities)
        
        initial_data = {
            'start_date': get_current_date(request.user),
            'end_date': get_current_date(request.user),
            'start_time': get_current_time(request.user),
            'end_time': get_midnight(request.user),
            'type': tipo_actividades,
        }

        actividades_form = ActivitiesForm(initial=initial_data)
        actividades_form.fields['type'].queryset = tipo_actividades
        context = {
            'percentage': total_percentage,
            'materia': materia,
            'grade': grade,
            'actividades': actividades_form,
            'vista': vista,
            'abierto':abierto,
            "tipo_actividades": tipo_actividades,
        }
        return render(request, 'users/teachers/activities/create_actividades.html', context)
    def post(self, request, pk, *args, **kwargs):
        actividades_form = ActivitiesForm(request.POST)
        #archivo_form = FileForm(request.POST, request.FILES)
        
        materia = Subjects.objects.get(pk=pk)
        author = request.user
        activities = Activities.objects.filter(author=author,subject=materia).values_list('percentage', flat=True)
        total_percentage = sum(activities)

        if actividades_form.is_valid():
        # Crear una instancia del modelo sin guardar en la base de datos aún
            actividad = actividades_form.save(commit=False)
            actividad.author = request.user  # Asigna el usuario actual como autor

            if total_percentage+actividad.percentage < 100:
                try:
                    materia_colegio = Subjects.objects.get(pk=pk)
                    actividad.subject = materia_colegio  # Asigna la materia a la actividad
                    
                    # Guarda la instancia del modelo en la base de datos
                    actividad.save()
                    messages.success(request, 'Actividad agregada correctamente!')
                    actividad_id = actividad.pk
                    return redirect('ViewActividades', pk=actividad_id)
                except Subjects.DoesNotExist:
                    messages.error(request, 'La materia especificada no existe')
                    return redirect('BoardTeachers')
                except TypeError:
                    messages.error(request, 'Verifica tus datos')
                    return redirect('BoardTeachers')
            else:
                messages.error(request, 'Superaste el 100% de la Asignatura!')
                return redirect('BoardTeachers')

        # Si el formulario no es válido, muestra los errores
        messages.error(request, 'Formulario no válido')
        return redirect('BoardTeachers')

def get_type_file(file):
    # Obtener el nombre del archivo desde la ruta completa
    file_name = file.name.split('/')[-1]  # Divide la ruta por '/' y toma el último segmento
    
    # Obtener la extensión del archivo
    ext = file_name.split('.')[-1].lower()  # Divide el nombre del archivo por '.' y toma la extensión

    
    if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']:
        return 'image'
    elif ext in ['pdf']:
        return 'pdf'
    elif ext in ['mp3', 'wav', 'ogg']:
        return 'audio'
    elif ext in ['mp4', 'avi', 'mov', 'webm']:
        return 'video'
    elif ext in ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
        return 'document'
    elif ext in ['txt', 'csv']:
        return 'text'
    else:
        return 'unknown'

# En esta vista los profesores pueden agregar archivos y ver a los estudiantes que respondeieron su actividad.
class ViewActividades(View):
    def get(self, request, pk, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        
        # Activity form / edit activity
        activity = Activities.objects.get(pk=pk)

        # Convertir los valores a strings en el formato correcto
        formatted_start_date = activity.start_date.strftime('%Y-%m-%d') if activity.start_date else ''
        formatted_end_date = activity.end_date.strftime('%Y-%m-%d') if activity.end_date else ''
        formatted_start_time = activity.start_time.strftime('%H:%M') if activity.start_time else ''
        formatted_end_time = activity.end_time.strftime('%H:%M') if activity.end_time else ''

        activity_form = ActivitiesForm(initial={
            'start_date': formatted_start_date,
            'end_date': formatted_end_date,
            'start_time': formatted_start_time,
            'end_time': formatted_end_time,
        }, instance=activity)


        #get Subject
        materia = activity.subject
        grado = Grade.objects.get(subjects=materia)
        
        students = CustomUserStudent.objects.filter(grade=grado)
        
        files = File.objects.filter(activity=pk)
        
        file_type = []
        # type of file
        for file in files:
            type = get_type_file(file.file)
            file_type.append(type)

        # group files
        all_files = zip(files, file_type)
        
        actividades_form = ActivitiesForm()

        try:
            respuestas = StudentResponse.objects.filter(activity=activity).select_related('author')

            # Ordenar las respuestas por el autor antes de agrupar
            respuestas = respuestas.order_by('author')

            # Agrupar las respuestas por el campo 'author' usando groupby
            respuestas_agrupadas = []

            autores_respondieron = []

            for author, respuestas_lista in groupby(respuestas, key=attrgetter('author')):
                respuestas_lista = list(respuestas_lista)  # generate a list
                try:
                    # Get student grade
                    rating = Rating.objects.get(student=author, activity=activity)
                    calificacion = rating.rating
                except ObjectDoesNotExist:
                    calificacion = None  # if is not grade, is None
                
                respuestas_agrupadas.append((author, respuestas_lista, calificacion))  # add student and activity
                autores_respondieron.append(author.pk)

            # Filter students who have not responded
            [respuestas_agrupadas.append((estudiante, [], None)) for estudiante in students if estudiante.pk not in autores_respondieron]

            # sort alphabetically
            respuestas_agrupadas.sort(key=lambda x: x[0].first_name.lower())
            
        except Exception as e:
            print(f"Error al obtener respuestas agrupadas: {e}")
            respuestas_agrupadas = None
            
        ## Students ratings
        StudentRatingsForm = RatingForm()

        final_date = activity.end_date
        final_hour = activity.end_time
        
        form = FilesProfesoresForm()
        
        context = {
            'StudentRatingForm': StudentRatingsForm,
            'students': students,
            'form': form,
            'files': all_files,
            'actividad': activity,
            'materia': materia,
            'grado': grado,
            'actividades': actividades_form,
            'vista': vista,
            'abierto':abierto,
            'respuestas_agrupadas': respuestas_agrupadas,
            'final_date': final_date,
            'final_hour': final_hour,
            'activityForm': activity_form,
        }
        return render(request, 'users/teachers/activities/view_actividades.html', context)
    def post(self, request, pk):
        form = FilesProfesoresForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            archivo = form.save(commit=False)
            actividad = Activities.objects.get(pk=pk)
            archivo.activity = actividad
            archivo.save()
            return redirect('ViewActividades', pk=pk)
        return redirect('ViewActividades', pk=pk)
    
class RatingStudentActivity(View):
    def post(self, request, student_pk, activity_pk, *args, **kwargs):
        try:
            ratingsForm = RatingForm(request.POST)

            if not ratingsForm.is_valid():
                return JsonResponse({
                    'message': 'Error en el formulario',
                    'errors': ratingsForm.errors,  # Ahora enviamos los errores al frontend
                    'status': 0
                }, status=400)

            teacher = request.user
            student = get_object_or_404(CustomUser, pk=student_pk)
            activity = get_object_or_404(Activities, pk=activity_pk)

            with transaction.atomic():  # Evita inconsistencias en la base de datos
                rating, created = Rating.objects.get_or_create(
                    teacher=teacher, student=student, activity=activity,
                    defaults={'rating': ratingsForm.cleaned_data['rating'], 'message': ratingsForm.cleaned_data['message']}
                )

                if not created:  # Si ya existía, actualizarla
                    rating.rating = ratingsForm.cleaned_data['rating']
                    rating.message = ratingsForm.cleaned_data['message']
                    rating.save()

            return JsonResponse({'message': 'Calificación guardada correctamente', 'status': 1})

        except Exception as e:
            print(f"Error en la vista RatingStudentActivity: {e}")  # Esto aparecerá en la terminal
            return JsonResponse({'message': 'Error interno del servidor', 'error': str(e), 'status': 0}, status=500)


    
    
class EditActividades(View):
    def post(self, request, pk, *args, **kwargs):
        activity = get_object_or_404(Activities, id=pk)

        form = ActivitiesForm(request.POST, instance=activity) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Formulario válido')
        else:
            messages.error(request, 'Formulario no válido')
        return redirect('BoardTeachers')
    
# Horario para dictar clases de profresores...
class ProfessorSchedule(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        subject_profesor = Subjects.objects.filter(teacher_1_id=user) | Subjects.objects.filter(teacher_2_id=user)
        grades = Grade.objects.filter(subjects__in=subject_profesor).distinct()

        schedules = DailySchedule.objects.filter(grade__in=grades).order_by('start_time')

        # Obtener la zona horaria del usuario
        user_zone = pytz.timezone(request.user.time_zone)
        
        # Obtener el día de la semana en la zona horaria del usuario
        day = timezone.now().astimezone(user_zone).strftime('%A')
        
        # Traducir el día al español si es necesario
        # Transalate day
        day_number_text = {
            "Monday": "1",
            "Tuesday": "2",
            "Wednesday": "3",
            "Thursday": "4",
            "Friday": "5",
            "Saturday": "6",
            "Sunday": "7",
        }
        day_numer = day_number_text.get(day, day)
        
        vista = 'profesores'
        abierto = 'calendario'
        context = {
            'user': user,
            'vista': vista,
            'abierto': abierto,
            'schedules': schedules,
            'day': day_numer,
        }
        
        return render(request, 'users/teachers/schedule/schedule.html', context)