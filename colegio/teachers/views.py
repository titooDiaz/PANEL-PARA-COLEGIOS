from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from information.models import Subjects, Grade, Activities, File, ActivitiesType, StudentResponse, DailySchedule
from .forms import ActivitiesForm, FileForm, FilesProfesoresForm
from django.contrib import messages
## MENSAJES DE ERRORES ##
from message_error import messages_error

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


class BoardProfesores(View):
    
    def get(self, request, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        profesor = request.user.pk
        materias_profesor = Subjects.objects.filter(teacher_1_id=profesor) | Subjects.objects.filter(teacher_2_id=profesor)
        grades = Grade.objects.filter(subjects__in=materias_profesor).distinct()
        actividades = Activities.objects.filter(subject__in=materias_profesor)

        # Obtener la zona horaria local
        zona_horaria_usuario = pytz.timezone(request.user.time_zone)

        # Obtener la hora actual en la zona horaria del usuario
        fecha_actual = datetime.now(zona_horaria_usuario).date()
        hora_actual = datetime.now(zona_horaria_usuario).time()
        print(actividades)
            
        context = {
            'grades': grades,
            'materias_profesor': materias_profesor,
            'vista': vista,
            'abierto':abierto,
            'actividades': actividades,
            'hora_actual': hora_actual,
            'fecha_actual': fecha_actual,
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
        grado = Grade.objects.get(subjects=materia)
        tipo_actividades = ActivitiesType.objects.filter(school_id=request.user.school)
        
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
            'materia': materia,
            'grado': grado,
            'actividades': actividades_form,
            'vista': vista,
            'abierto':abierto,
            "tipo_actividades": tipo_actividades,
        }
        return render(request, 'users/teachers/activities/create_actividades.html', context)
    def post(self, request, pk, *args, **kwargs):
        actividades_form = ActivitiesForm(request.POST)
        #archivo_form = FileForm(request.POST, request.FILES)

        if actividades_form.is_valid():
        # Crear una instancia del modelo sin guardar en la base de datos aún
            actividad = actividades_form.save(commit=False)
            actividad.author = request.user  # Asigna el usuario actual como autor

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
                return redirect('BoardProfesores')
            except TypeError:
                messages.error(request, 'Verifica tus datos')
                return redirect('BoardProfesores')

        # Si el formulario no es válido, muestra los errores
        messages.error(request, 'Formulario no válido')
        return redirect('BoardProfesores')

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
        activity = Activities.objects.get(pk=pk)
        #obtener materia
        materia = activity.subject
        grado = Grade.objects.get(subjects=materia)
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
            # Obtener las respuestas relacionadas con una actividad específica
            respuestas = StudentResponse.objects.filter(activity=activity).select_related('author')

            # Ordenar las respuestas por el autor antes de agrupar
            respuestas = respuestas.order_by('author')

            # Agrupar las respuestas por el campo 'author' usando groupby
            respuestas_agrupadas = [(author, list(respuestas)) for author, respuestas in groupby(respuestas, key=attrgetter('author'))]
        except:
            respuestas_agrupadas = None
        
        final_date = activity.end_date
        final_hour = activity.end_time
        
        form = FilesProfesoresForm()
        context = {
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
    
class EditActividades(View):
    def get(self, request, pk, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        materia = Subjects.objects.get(pk=pk)
        grado = Grade.objects.get(materias=materia)

        actividades_tipo = ActivitiesType.objects.filter(colegio=request.user.school)
        
        initial_data = {
            'fecha_inicio': get_current_date(request.user),
            'fecha_final': get_current_date(request.user),
            'hora_inicio': get_current_time(request.user),
            'hora_final': get_midnight(request.user),
            'tipo': actividades_tipo,
        }
        actividades_form = ActivitiesForm(initial=initial_data)
        print(materia.titulo1,"  -  ")
        context = {
            'materia': materia,
            'grado': grado,
            'actividades': actividades_form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/teachers/activities/create_actividades.html', context)
    def post(self, request, pk, *args, **kwargs):
        actividades_form = ActivitiesForm(request.POST)

        if actividades_form.is_valid():
        # Crear una instancia del modelo sin guardar en la base de datos aún
            actividad = actividades_form.save(commit=False)
            actividad.author = request.user  # Asigna el usuario actual como autor

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
                return redirect('BoardProfesores')
            except TypeError:
                messages.error(request, 'Verifica tus datos')
                return redirect('BoardProfesores')

        # Si el formulario no es válido, muestra los errores
        messages.error(request, 'Formulario no válido')
        return redirect('BoardProfesores')
    
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