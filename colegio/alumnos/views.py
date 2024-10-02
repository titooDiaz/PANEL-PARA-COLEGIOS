from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View    
from informacion.models import Actividades, Grado
from django.shortcuts import render, redirect
from django.views import View
from informacion.models import Actividades_Respuesta_Estudiantes, Archivo
from .forms import ActividadesRespuestaForm

# LIBRERIAS DE FECHAS
from datetime import datetime
import pytz
import time
import tzlocal #pip install tzlocal


class AlumnoBoard(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='inicio'
        
        user = request.user
        
        #vista de estudiantes (obviamente tiene modelo de estudiante)
        grado_user = user.customuseralumno.grado #grado del estudiante
        materias_user = grado_user.materias.all() #materias del estudainte
        actividades_user = Actividades.objects.filter(materia__in=materias_user)
        
        ## Obtener la zona horaria local
        zona_horaria_usuario = pytz.timezone(request.user.time_zone)

        # Obtener la hora actual en la zona horaria del usuario
        fecha_actual = datetime.now(zona_horaria_usuario).date()
        hora_actual = datetime.now(zona_horaria_usuario).time()
        
        context = {
            'vista': vista,
            'abierto':abierto,
            'grado': grado_user,
            'materias': materias_user,
            'actividades': actividades_user,
            'fecha_actual': fecha_actual,
            'hora_actual': hora_actual,
            
        }
        return render(request, 'users/alumnos/inicio.html', context)
    
class ActividadesRespuestaView(View):
    def get(self, request, *args, **kwargs):
        form = ActividadesRespuestaForm()
        return render(request, 'users/alumnos/actividades/responder.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ActividadesRespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.author = request.user
            respuesta.save()
            for archivo in request.FILES.getlist('archivos'):
                Archivo.objects.create(actividad_respuesta=respuesta, archivo=archivo)
            return redirect('success_url')
        return render(request, 'users/alumnos/actividades/responder.html', {'form': form})
    
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