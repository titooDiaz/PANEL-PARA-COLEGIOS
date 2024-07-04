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
    
class ViewActividades(View):
    def get(self, request, pk, *args, **kwargs):
        vista = 'profesores'
        abierto='inicio'
        actividades_form = ActividadesForm()
        materia = Materias.objects.get(pk=pk)
        grado = Grado.objects.get(materias=materia)
        print(grado)
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