from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View    
from informacion.models import Actividades, Grado, Materias
from django.shortcuts import render, redirect
from django.views import View
from informacion.models import Actividades_Respuesta_Estudiantes, Archivo
from .forms import ActividadesRespuestaForm

# LIBRERIAS DE FECHAS
from datetime import datetime
import pytz
import time
import tzlocal #pip install tzlocal


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
        grado_user = user.customuseralumno.grado #grado del estudiante
        materias_user = grado_user.materias.all() #materias del estudainte
        
        
        ## Obtener la zona horaria local
        zona_horaria_usuario = pytz.timezone(request.user.time_zone)
        
        # Obtener la hora actual en la zona horaria del usuario
        fecha_actual = datetime.now(zona_horaria_usuario).date()
        hora_actual = datetime.now(zona_horaria_usuario).time()
        
        
        actividades_user_on_time = Actividades.objects.filter(
            materia__in=materias_user,
            fecha_final__gt=fecha_actual
        )
        
        
        actividades_user_off_time = Actividades.objects.filter(
            materia__in=materias_user,
            fecha_final__lte=fecha_actual
        )
    
        
        context = {
            'vista': vista,
            'abierto':abierto,
            'grado': grado_user,
            'materias': materias_user,
            'actividades': actividades_user_on_time,
            'actividades_pasadas': actividades_user_off_time,
            'fecha_actual': fecha_actual,
            'hora_actual': hora_actual,
            
        }
        return render(request, 'users/alumnos/inicio.html', context)
    
class ActividadesRespuestaView(View):
    def get(self, request, pk, *args, **kwargs):
        form = ActividadesRespuestaForm()
        
        #Seleccionar frase para el estudiante
        frase = random.choice(mensajes_motivadores)
        
        # Obtener materia
        actividad = Actividades.objects.get(pk=pk)
        
        # Retorno del contexto
        vista = 'estudiante'
        abierto='calendario'
        context = {
            'vista': vista,
            'abierto':abierto,
            'form': form,
            'frase': frase,
            'actividad': actividad,
        }
        return render(request, 'users/alumnos/actividades/responder.html', context)

    def post(self, request, pk, *args, **kwargs):
        form = ActividadesRespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.author = request.user
            respuesta.save()
            for archivo in request.FILES.getlist('archivos'):
                Archivo.objects.create(actividad_respuesta=respuesta, archivo=archivo)
                
            # Retorno del contexto
            context = {
                'form': form
            }
            return redirect('success_url')
            
        return render(request, 'users/alumnos/actividades/responder.html', context)
    
class AlumnoCalendario(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='calendario'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/inicio.html', context)
    
class AlumnoMensajes(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='mensajes'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/inicio.html', context)
    
class AlumnoPersonas(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='personas'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/inicio.html', context)
    
class AlumnoNotas(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='notas'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/inicio.html', context)