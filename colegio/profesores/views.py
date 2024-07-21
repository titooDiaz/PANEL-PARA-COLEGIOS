from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from informacion.models import Materias, Grado, Actividades, Archivo
from .forms import ActividadesForm, ArchivoForm
from django.contrib import messages
## MENSAJES DE ERRORES ##
from message_error import messages_error


class BoardProfesores(View):
    def get(self, request, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        profesor = request.user.pk
        materias_profesor = Materias.objects.filter(profe1=profesor) | Materias.objects.filter(profe2=profesor)
        grados = Grado.objects.filter(materias__in=materias_profesor).distinct()
        actividades = Actividades.objects.filter(materia__in=materias_profesor)
        context = {
            'grados': grados,
            'materias_profesor': materias_profesor,
            'vista': vista,
            'abierto':abierto,
            'actividades': actividades,
        }
        return render(request, 'users/profesores/inicio.html', context)


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
    midnight_user_tz = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight_user_tz



class CreateActividades(View):
    def get(self, request, pk, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        materia = Materias.objects.get(pk=pk)
        grado = Grado.objects.get(materias=materia)

        initial_data = {
            'fecha_inicio': get_current_date(request.user),
            'fecha_final': get_current_date(request.user),
            'hora_inicio': get_current_time(request.user),
            'hora_final': get_midnight(request.user),
        }
        actividades_form = ActividadesForm(initial=initial_data)
        print(materia.titulo1,"  -  ")
        context = {
            'materia': materia,
            'grado': grado,
            'actividades': actividades_form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/profesores/actividades/create_actividades.html', context)
    def post(self, request, pk, *args, **kwargs):
        actividades_form = ActividadesForm(request.POST)
        #archivo_form = ArchivoForm(request.POST, request.FILES)

        if actividades_form.is_valid():
        # Crear una instancia del modelo sin guardar en la base de datos aún
            actividad = actividades_form.save(commit=False)
            actividad.author = request.user  # Asigna el usuario actual como autor

            try:
                materia_colegio = Materias.objects.get(pk=pk)
                actividad.materia = materia_colegio  # Asigna la materia a la actividad
                
                # Guarda la instancia del modelo en la base de datos
                actividad.save()
                messages.success(request, 'Actividad agregada correctamente!')
            except Materias.DoesNotExist:
                messages.error(request, 'La materia especificada no existe')
                return redirect('BoardProfesores')
            except TypeError:
                messages.error(request, 'Verifica tus datos')
                return redirect('BoardProfesores')
            
            return redirect('BoardProfesores')

        # Si el formulario no es válido, muestra los errores
        messages.error(request, 'Formulario no válido')
        return redirect('BoardProfesores')
    
class EditActividades(View):
    def get(self, request, pk, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        materia = Materias.objects.get(pk=pk)
        grado = Grado.objects.get(materias=materia)

        initial_data = {
            'fecha_inicio': get_current_date(request.user),
            'fecha_final': get_current_date(request.user),
            'hora_inicio': get_current_time(request.user),
            'hora_final': get_midnight(request.user),
        }
        actividades_form = ActividadesForm(initial=initial_data)
        print(materia.titulo1,"  -  ")
        context = {
            'materia': materia,
            'grado': grado,
            'actividades': actividades_form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/profesores/actividades/create_actividades.html', context)
    def post(self, request, pk, *args, **kwargs):
        actividades_form = ActividadesForm(request.POST)
        #archivo_form = ArchivoForm(request.POST, request.FILES)

        if actividades_form.is_valid():
        # Crear una instancia del modelo sin guardar en la base de datos aún
            actividad = actividades_form.save(commit=False)
            actividad.author = request.user  # Asigna el usuario actual como autor

            try:
                materia_colegio = Materias.objects.get(pk=pk)
                actividad.materia = materia_colegio  # Asigna la materia a la actividad
                
                # Guarda la instancia del modelo en la base de datos
                actividad.save()
                messages.success(request, 'Actividad agregada correctamente!')
            except Materias.DoesNotExist:
                messages.error(request, 'La materia especificada no existe')
                return redirect('BoardProfesores')
            except TypeError:
                messages.error(request, 'Verifica tus datos')
                return redirect('BoardProfesores')
            
            return redirect('BoardProfesores')

        # Si el formulario no es válido, muestra los errores
        messages.error(request, 'Formulario no válido')
        return redirect('BoardProfesores')