from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View    
from information.models import Activities, Subjects
from django.views import View
from information.models import StudentResponse, File, StudentFiles, DailySchedule, School, Grade
from .forms import ActivitiesAnswerForm
from django.contrib import messages
from information.models import Rating
from users.models import *
from information.forms import *
from .forms import *
from users.forms import *
from users.utils import is_user_online
from django.core.paginator import Paginator
from users.utils import get_chat_target, get_user_role, get_user1_user2_ids
from django.db.models import Q

# LIBRERIAS DE FECHAS
from django.utils import timezone
import pytz
from datetime import datetime 

# keep session auth
from django.contrib.auth import update_session_auth_hash

# time now!
from utils.functions import time_zone_user_location

# Frases motivadoras
import random
mensajes_motivadores = [
    "¡Genial! Empezar a revisar tus tareas es un gran paso para terminarlas.",
    "Cada página que repasas es un paso más cerca de alcanzar tus metas.",
    "¡Vas muy bien! Todo pequeño esfuerzo te lleva más cerca del éxito.",
    "Recuerda, no se trata de hacerlo rápido, sino de hacerlo bien. ¡Sigue así!",
    "Estás construyendo tu futuro, una tarea a la vez. ¡Sigue adelante!",
    "Cada minuto que inviertes ahora, es un regalo para tu yo del futuro.",
    "El camino puede ser largo, pero cada paso que das es progreso. ¡No te detengas!",
    "Estás más cerca de lo que piensas. ¡Confía en ti mismo y sigue avanzando!",
    "El esfuerzo de hoy es la recompensa de mañana. ¡Lo estás haciendo excelente!",
    "Si te sientes abrumado, recuerda lo lejos que ya has llegado. ¡Sigue adelante!",
    "No importa cuán lento avances, lo importante es que sigas moviéndote hacia adelante.",
    "El éxito no se mide por la velocidad, sino por la constancia. ¡Tú puedes!",
    "Cada desafío que enfrentas ahora es una oportunidad para aprender y mejorar.",
    "Lo que haces hoy puede parecer pequeño, pero está construyendo algo grande para mañana.",
    "Respira hondo y sigue. Cada esfuerzo cuenta, y cada paso te acerca a tus objetivos.",
    "No hay esfuerzo inútil. Cada minuto que dedicas es un ladrillo en el camino hacia tu éxito.",
    "Toma un descanso si lo necesitas, pero no te rindas. ¡Estás haciendo un gran trabajo!",
    "Aprender no es fácil, pero la satisfacción de haberlo hecho bien valdrá todo el esfuerzo.",
    "¡Vamos! Cada tarea completada es una victoria. ¡Sigue acumulando logros!",
    "Recuerda que las mejores cosas toman tiempo. Tu esfuerzo dará frutos, ¡confía en el proceso!"
]

class AlumnoBoard(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='inicio'
        
        user = request.user
        
        #vista de estudiantes (obviamente tiene modelo de estudiante)
        grade_user = user.customuserstudent.grade #student's grade
        materias_user = grade_user.subjects.all() #materias del estudainte
        
        
        # Obtener la hora actual en la zona horaria del usuario
        ## Obtener la zona horaria local
        fecha_actual, hora_actual = time_zone_user_location(request.user.time_zone)
        
        
        actividades_user_on_time = Activities.objects.filter(
            subject__in=materias_user,
            end_date__gte=fecha_actual
        )
        
        
        actividades_user_off_time = Activities.objects.filter(
            subject__in=materias_user,
            end_date__lte=fecha_actual
        )
        
        # grade for each activity
        actividades_user_off_time_grade = []
        for activity in actividades_user_off_time:
            grade = Rating.objects.filter(student=request.user, activity=activity).first()
            actividades_user_off_time_grade.append(grade)

        actividades_user_off_time = zip(actividades_user_off_time_grade, actividades_user_off_time)
    
        
        context = {
            'vista': vista,
            'abierto':abierto,
            'grade': grade_user,
            'materias': materias_user,
            'actividades': actividades_user_on_time,
            'activityOff': actividades_user_off_time,
            'fecha_actual': fecha_actual,
            'hora_actual': hora_actual,
            
        }
        return render(request, 'users/student/home.html', context)

class ActividadesRespuestaView(View):
    def get(self, request, pk, *args, **kwargs):
        
        ## Obtener la zona horaria local
        fecha_actual, hora_actual = time_zone_user_location(request.user.time_zone)
        
        #vista de estudiantes (obviamente tiene modelo de estudiante)
        user = request.user
        grade_user = user.customuserstudent.grade #student's grade
        materias_user = grade_user.subjects.all() #materias del estudainte
        
        actividades_user_on_time = Activities.objects.filter(
            subject__in=materias_user,
            end_date__gte=fecha_actual
        )
        
        actividades_user_off_time = Activities.objects.filter(
            subject__in=materias_user,
            end_date__lte=fecha_actual
        )
        
        activity = Activities.objects.get(pk=pk)
        # Extraer los datos de los campos
        date = activity.end_date # Esto es un objeto date (año, mes, día)
        hour = activity.end_time    # Esto es un objeto time (hora, minuto, segundo, etc.)

        combined_datetime = datetime.combine(date, hour)
        
        # on_time
        # 1 --> On time
        # 2 --> Out time
        # 3 --> on time (today)
        
        if activity in actividades_user_off_time:
            if activity.end_time > hora_actual and activity.end_date >= fecha_actual:
                # on time (Today)
                on_time = 3
            else:
                # the time has ended
                on_time = 2
        elif activity in actividades_user_on_time:
            # They still have plenty of time
            on_time = 1
        else:
            # This case should never exist, but if something fails we will have to say that it is too late to upload it.
            on_time = 2
            
        #User activity...
        user = request.user
        user_answers = StudentResponse.objects.filter(activity=activity.pk)
            
        # Grade
        grade_user = user.customuserstudent.grade #student's grade
        
        form = ActivitiesAnswerForm()
        
        #Seleccionar frase para el estudiante
        frase = random.choice(mensajes_motivadores)
        
        # Obtener materia
        actividad = Activities.objects.get(pk=pk)
        
        # Get grade
        grade = Rating.objects.filter(student=request.user, activity=activity).first()
        
        # Retorno del contexto
        vista = 'estudiante'
        abierto='inicio'
        context = {
            'vista': vista,
            'abierto':abierto,
            'form': form,
            'frase': frase,
            'actividad': actividad,
            'grade': grade_user,
            'date': combined_datetime.isoformat(),
            'on_time': on_time,
            'answers': user_answers,
            'rating': grade,
        }
        return render(request, 'users/student/activities/answers.html', context)

    def post(self, request, pk, *args, **kwargs):
        form = ActivitiesAnswerForm(request.POST, request.FILES)
        #time zone info
        nowDate, nowTime = time_zone_user_location(request.user.time_zone)
        if form.is_valid():
            # process of save instance
            student_response_instance = form.save(commit=False)
            student_response_instance.delivery_date = nowDate
            student_response_instance.delivery_time = nowTime
            student_response_instance.timezone_response = request.user.time_zone
            student_response_instance.author = request.user
            student_response_instance.activity = Activities.objects.get(pk=pk)
            student_response_instance.save()
            
            # Obtén la instancia de StudentResponse recién creada
            student_response_instance = student_response_instance
            
            archivos_publicados = ""
            for archivo in request.FILES.getlist('archivo'):
                archivos_publicados = "\n - " + archivo.name + archivos_publicados
                # Pasa la instancia de StudentResponse en lugar del ID
                StudentFiles.objects.create(activity_answer=student_response_instance, file=archivo)
            
            messages.success(request, f'Wow! Subiste todo correctamente! \n Tus archivos: {archivos_publicados}')
            return redirect('ResponderActividades', pk)
        
        return redirect('ResponderActividades', pk)

#Subjects View
class SubjectsView(View):
    def get(self, request, pk, *args, **kwargs):
        # Grade
        user = request.user
        grade_user = user.customuserstudent.grade #student's grade
        subject = Subjects.objects.get(pk=pk)
        
        vista = 'estudiante'
        abierto='inicio'
        context = {
            'vista': vista,
            'abierto':abierto,
            'grade': grade_user,
            'subject':subject,
        }
        return render(request, 'users/student/subjects/subjects.html', context)
    
class AlumnoCalendario(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        grade_user = user.customuserstudent.grade 
        horario = DailySchedule.objects.filter(grade=grade_user)
        
        # Obtener la zona horaria del usuario
        user_zone = pytz.timezone(request.user.time_zone)
        
        # Obtener el día de la semana en la zona horaria del usuario
        day = timezone.now().astimezone(user_zone).strftime('%A')
        
        # Traducir el día al español si es necesario
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
        
        vista = 'estudiante'
        abierto = 'calendario'
        context = {
            'user': user,
            'vista': vista,
            'abierto': abierto,
            'horario': horario,
            'day': day_numer,
            'grade': grade_user,
        }
        
        return render(request, 'users/student/schedule/schedule.html', context)

class StudentMessages(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        grade_user = user.customuserstudent.grade
        school_user = grade_user.school
        teachers = CustomUserTeachers.objects.filter(school=school_user)
        students = CustomUserStudent.objects.filter(grade=grade_user)

        selected_user = get_chat_target(request)
        messages = []
        form = ChatMessageForm()
        user1_id, user2_id = None, None
        
        if selected_user:
            all_messages = ChatMessage.objects.filter(
                Q(sender=user, receiver=selected_user) |
                Q(sender=selected_user, receiver=user)
            ).order_by('-sent_at')
            paginator = Paginator(all_messages, 15)
            page = paginator.get_page(1)
            messages = list(page.object_list)[::-1]
        
            user1_id, user2_id = get_user1_user2_ids(user, selected_user)
            
        context = {
            'vista': 'estudiante',
            'abierto': 'mensajes',
            'grade': grade_user,
            'teachers': teachers,
            'students': students,
            'selected_user': selected_user,
            'messages_users': messages,
            'form': form,
            'user1Id': user1_id,
            'user2Id': user2_id,
        }
        return render(request, 'users/student/messages/messages.html', context)

class StudentPeople(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='personas'
        
        # Grade
        user = request.user
        grade_user = user.customuserstudent.grade #student's grade
        
        context = {
            'vista': vista,
            'abierto':abierto,
            'grade': grade_user,
        }
        return render(request, 'users/student/people/people.html', context)
    
class StudentGrades(View):
    def get(self, request, *args, **kwargs):
        # Grade
        user = request.user
        grade_user = user.customuserstudent.grade # student's grade
        
        vista = 'estudiante'
        abierto='notas'
        
        context = {
            'vista': vista,
            'abierto':abierto,
            'grade': grade_user,
        }
        return render(request, 'users/student/grades/grades.html', context)

# View profile
class ViewProfile(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        vista = 'estudiante'
        abierto='personas'
        editForm = CustomUserStudentEditProfileForm(instance=user)
        editPasswordForm = CustomPasswordChangeForm(user=user)
        grade_user = user.customuserstudent.grade #student's grade
        context = {
            'vista': vista,
            'abierto':abierto,
            'user':user,
            'editProfile': editForm,
            'editPassword': editPasswordForm,
            'grade': grade_user,
        }
        return render(request, 'users/student/profile.html', context)
    def post(self, request, *args, **kwargs):
        user = request.user
        formProfile = CustomUserStudentEditProfileForm(request.POST, instance=user)
        
        if formProfile.is_valid():
            formProfile.save()
            messages.success(request, 'Perfil actualizado correctamente')
        else:
            messages.error(request, 'Error al editar el perfil.')
        return redirect('ViewProfileStudent')

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
        return redirect('ViewProfileStudent')    