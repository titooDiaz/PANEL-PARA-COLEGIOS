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
        context = {
            'grados': grados,
            'materias_profesor': materias_profesor,
            'vista': vista,
            'abierto':abierto,
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



class ViewActividades(View):
    def get(self, request, pk, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        materia = Materias.objects.get(pk=pk)
        grado = Grado.objects.get(materias=materia)
        print(grado)
        initial_data = {
            'fecha_inicio': get_current_date(request.user),
            'fecha_final': get_current_date(request.user),
            'hora_inicio': get_current_time(request.user),
            'hora_final': get_current_time(request.user),
        }
        actividades_form = ActividadesForm(initial=initial_data)
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
            actividades_form.save(commit=False)
            try:
                materia = Materias.objects.get(pk=pk)
                actividades_form.materia = materia
                actividades_form.author = request.user.pk
            except:
                messages.success(request, 'Verifica tus datos')
                return redirect('BoardProfesores')
            return redirect('BoardProfesores')