# Django utilities for rendering templates and handling redirects
from django.shortcuts import render, redirect

# Django class-based views
from django.views.generic import TemplateView, View

from django.core.paginator import Paginator

# Import models related to subjects, grades, activities, schedules, and ratings
from information.models import (
    Subjects, Grade, Activities, File, ActivitiesType, StudentResponse, 
    DailySchedule, Rating, ScheduleParts, ScheduleCourts
)

# Import forms for handling activities, file uploads, and ratings
from .forms import ActivitiesForm, FileForm, FilesProfesoresForm, RatingForm

# Django messaging framework for displaying notifications to users
from django.contrib import messages

# Custom error messages module
from message_error import messages_error

# Optimized database queries
from django.db.models import Prefetch

# Exception handling for missing objects
from django.core.exceptions import ObjectDoesNotExist

# Utilities for grouping query results
from itertools import groupby
from operator import attrgetter

# Function to get objects or return a 404 error if not found
from django.shortcuts import get_object_or_404

# Ensures database operations are performed atomically (to prevent inconsistencies)
from django.db import transaction

# Custom user models for teachers and students
from users.models import CustomUser, CustomUserStudent, CustomUserTeachers

# Define aliases for user models
UserProfes = CustomUserTeachers  # Teachers
UserAlumno = CustomUserStudent   # Students

# Django utility for returning JSON responses (useful for AJAX and real-time updates)
from django.http import JsonResponse

# Library for handling file system operations
import os

# Django authentication system
from django.contrib.auth import get_user_model

# Utilities for counting, grouping, and aggregating data
from itertools import groupby
from operator import attrgetter
from django.db.models import Count
from collections import defaultdict

# Date and time utilities
from datetime import datetime
import pytz
import time
import tzlocal  # Library for detecting the local timezone (install with `pip install tzlocal`)

# Function for getting the user's time zone from the utils module
from utils.functions import time_zone_user_location

# keep session auth
from django.contrib.auth import update_session_auth_hash

from .forms import *
from users.forms import *
from information.models import ChatMessage
from information.forms import ChatMessageForm


class BoardTeachers(View):
    def get(self, request, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        teacher = request.user.pk
        materias_teacher = Subjects.objects.filter(teacher_1_id=teacher) | Subjects.objects.filter(teacher_2_id=teacher)
        grades = Grade.objects.filter(subjects__in=materias_teacher).distinct()
        
        # What is my court?
        grades_list = []
        for grade in grades:
            schedule = grade.schedule_parts
            # get current schedule part.
            court = ScheduleCourts.objects.filter(schedule=schedule).first()
            data_time = get_current_date(request.user)
            data_court = court.get_current_court(request.user, schedule, data_time)
            grades_list.append((grade, data_court))
            
        actividades = Activities.objects.filter(subject__in=materias_teacher)

        #Time zone
        DateNow, TimeNow = time_zone_user_location(request.user.time_zone)
            
        context = {
            'grades': grades_list,
            'materias_profesor': materias_teacher,
            'vista': vista,
            'abierto':abierto,
            'actividades': actividades,
            'hora_actual': TimeNow,
            'fecha_actual': DateNow,
        }
        return render(request, 'users/teachers/board.html', context)


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
        # initial data for view!
        vista = 'profesores'
        abierto='inicio'
        materia = Subjects.objects.get(pk=pk)
        author = request.user
        grade = Grade.objects.filter(subjects=materia).first()
        
        # get percentage
        tipo_actividades = ActivitiesType.objects.filter(school_id=request.user.school)
        activities = Activities.objects.filter(author=author,subject=materia).values_list('percentage', flat=True)
        total_percentage = sum(activities)
        
        # get current court
        schedule = ScheduleParts.objects.filter(school_id=request.user.school).first()
        court = ScheduleCourts.objects.filter(schedule=schedule).first()
        data_time = get_current_date(request.user)
        data_court = court.get_current_court(author, schedule, data_time)
        
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
            'tipo_actividades': tipo_actividades,
            'current_court': data_court,
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

            if total_percentage+actividad.percentage <= 100:
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

def get_file_type(file):
    # Get the file name from the full path
    file_name = file.name.split('/')[-1]  # Splits the path by '/' and takes the last segment
    
    # Get the file extension
    ext = file_name.split('.')[-1].lower()  # Splits the file name by '.' and extracts the extension

    # Determine the file type based on its extension
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
            type = get_file_type(file.file)
            file_type.append(type)

        # group files
        all_files = zip(files, file_type)
        
        actividades_form = ActivitiesForm()

        try:
            respuestas = StudentResponse.objects.filter(activity=activity).select_related('author').order_by('author')

            respuestas_agrupadas = []
            autores_respondieron = set()  # Usamos un set para búsquedas rápidas

            # Agrupar respuestas por autor
            for author, respuestas_lista in groupby(respuestas, key=attrgetter('author')):
                respuestas_lista = list(respuestas_lista)
                try:
                    rating = Rating.objects.get(student=author, activity=activity)
                    calificacion = rating.rating
                except ObjectDoesNotExist:
                    calificacion = None

                respuestas_agrupadas.append((author, respuestas_lista, calificacion))
                autores_respondieron.add(author.pk)

            # Recorrer todos los estudiantes y agregar los que no han respondido
            for student in students:
                if student.pk not in autores_respondieron:
                    try:
                        rating = Rating.objects.get(student=student, activity=activity)
                        calificacion = rating.rating
                    except ObjectDoesNotExist:
                        calificacion = None
                    respuestas_agrupadas.append((student, [], calificacion))

            # Ordenar la lista alfabéticamente por el nombre del estudiante
            respuestas_agrupadas.sort(key=lambda x: x[0].first_name.lower())

        except Exception as e:
            respuestas_agrupadas = None  # En caso de error, manejarlo adecuadamente     
        ## Students ratings
        StudentRatingsForm = RatingForm()

        final_date = activity.end_date
        final_hour = activity.end_time
        
        form = FilesProfesoresForm()
        
        # get current court
        subject_id = activity.subject.pk
        subject = Subjects.objects.get(id=subject_id)
        grade = Grade.objects.filter(subjects=subject).first()
        grade = Grade.objects.get(id=grade.pk)
        schedule = grade.schedule_parts 
        court = ScheduleCourts.objects.filter(schedule=schedule).first()
        data_time = get_current_date(request.user)
        data_court = court.get_current_court(request.user, schedule, data_time)
        
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
            'current_court': data_court
        }
        return render(request, 'users/teachers/activities/view_actividades.html', context)
    
    def post(self, request, pk):
        form = FilesProfesoresForm(request.POST, request.FILES)
        
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
            ratings_form = RatingForm(request.POST)

            if not ratings_form.is_valid():
                return JsonResponse({
                    'message': 'Form error',
                    'errors': ratings_form.errors,  # Now sending errors to the frontend
                    'status': 0
                }, status=400)

            teacher = request.user
            student = get_object_or_404(CustomUser, pk=student_pk)
            activity = get_object_or_404(Activities, pk=activity_pk)

            with transaction.atomic():  # Prevents database inconsistencies
                rating, created = Rating.objects.get_or_create(
                    teacher=teacher, student=student, activity=activity,
                    defaults={'rating': ratings_form.cleaned_data['rating'], 'message': ratings_form.cleaned_data['message']}
                )

                if not created:  # Update if the rating already existed
                    rating.rating = ratings_form.cleaned_data['rating']
                    rating.message = ratings_form.cleaned_data['message']
                    rating.save()
                    
            return JsonResponse({'message': 'Rating saved successfully', 'status': 1})

        except Exception as e:
            print(f"Error in RatingStudentActivity view: {e}")  # This will appear in the terminal
            return JsonResponse({'message': 'Internal server error', 'error': str(e), 'status': 0}, status=500)

    
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
    
# Schedule for professors to teach classes...
class ProfessorSchedule(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        subject_professor = Subjects.objects.filter(teacher_1_id=user) | Subjects.objects.filter(teacher_2_id=user)
        grades = Grade.objects.filter(subjects__in=subject_professor).distinct()

        schedules = DailySchedule.objects.filter(grade__in=grades).order_by('start_time')

        # Get the user's time zone
        user_zone = pytz.timezone(request.user.time_zone)
        
        # Get the current weekday in the user's time zone
        day = timezone.now().astimezone(user_zone).strftime('%A')
        
        # Translate the day to a numerical representation
        day_number_map = {
            "Monday": "1",
            "Tuesday": "2",
            "Wednesday": "3",
            "Thursday": "4",
            "Friday": "5",
            "Saturday": "6",
            "Sunday": "7",
        }
        day_number = day_number_map.get(day, day)
        
        view = 'profesores'
        open_section = 'calendario'
        context = {
            'user': user,
            'vista': view,
            'abierto': open_section,
            'schedules': schedules,
            'day': day_number,
        }
        
        return render(request, 'users/teachers/schedule/schedule.html', context)

class ProfessorMessages(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        school_user = user.school
        students = CustomUserStudent.objects.filter(school=school_user)

        selected_student_id = request.GET.get('student_id')
        selected_student = None
        messages = []
        form = ChatMessageForm()

        if selected_student_id:
            selected_student = get_object_or_404(CustomUserStudent, pk=selected_student_id)

            chat_qs = ChatMessage.objects.filter(
                sender__in=[user, selected_student],
                receiver__in=[user, selected_student]
            ).order_by('-sent_at')

            paginator = Paginator(chat_qs, 25)
            first_page = paginator.page(1)
            messages = list(first_page.object_list)[::-1]  # ⚠️ Importante para que el scroll funcione bien

        context = {
            'vista': 'profesores',
            'abierto': 'mensajes',
            'students': students,
            'selected_user': selected_student,
            'messages_users': messages,
            'form': form,
        }
        return render(request, 'users/teachers/messages/messages.html', context)

    
class ProfessorPeople(View):
    def get(self, request, *args, **kwargs):
        view = 'profesores'
        open_section = 'personas'
        context = {
            'vista': view,
            'abierto': open_section,
        }
        
        return render(request, 'users/teachers/people/people.html', context)

class ProfessorRatings(View):
    def get(self, request, *args, **kwargs):
        view = 'profesores'
        open_section = 'notas'
        context = {
            'vista': view,
            'abierto': open_section,
        }
        
        return render(request, 'users/teachers/rating/ratings.html', context)
    
# View profile
class ViewProfile(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        vista = 'profesores'
        abierto='personas'
        editForm = CustomUserTeacherEditProfileForm(instance=user)
        editPasswordForm = CustomPasswordChangeForm(user=user)
        context = {
            'vista': vista,
            'abierto':abierto,
            'user':user,
            'editProfile': editForm,
            'editPassword': editPasswordForm,
        }
        return render(request, 'users/teachers/profile.html', context)
    def post(self, request, *args, **kwargs):
        user = request.user
        formProfile = CustomUserTeacherEditProfileForm(request.POST, instance=user)
        
        if formProfile.is_valid():
            formProfile.save()
            messages.success(request, 'Perfil actualizado correctamente')
        else:
            messages.error(request, 'Error al editar el perfil.')
        return redirect('ViewProfileTeacher')

class ChangePassword(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        formPassword = CustomPasswordChangeForm(user=user, data=request.POST)
        if formPassword.is_valid():
            formPassword.save()
            messages.success(request, 'Contraseña actualizada correctamente')
            update_session_auth_hash(request, user)
        else:
            messages.error(request, formPassword.errors)
        return redirect('ViewProfileTeacher')        