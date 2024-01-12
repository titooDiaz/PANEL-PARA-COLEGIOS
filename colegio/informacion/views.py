from django.shortcuts import render, get_object_or_404, redirect
from .models import Grado, HorarioDiario
from django.views.generic import TemplateView, View

from .forms import HoraHorarioForm, MateriasHorarioForm

class VerGrados(View):
    def get(self, request, *args, **kwargs):
        grados = Grado.objects.all()
        print(grados)
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'grados': grados,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/grados/ver_grados.html', context)
    

"""VISTA INICIAL
VAMOS A USAR 'APIS', PARA NO SOBRECARGAR LA VISTA

LAS 'APIS' ESTAN ABAJO DE LA CLASE VerGradosHorario... 
PARA CADA MOVIMIENTO HYA UNA VISTA DEDICADA, QUE RETORNARA ESTA MISMA VISTA
         |
        \|/
"""
class VerGradosHorario(View):
    def get(self, request, pk, *args, **kwargs):
        grado = Grado.objects.get(id=pk)
        horarios_del_grado = HorarioDiario.objects.filter(grado=grado)
        vista = 'gestor'
        abierto='ajustes'

        #filtrar materias
        materias_grado = grado.materias.all()
        """DEBEMOS CREAR UN FORMULARIO POR CADA ELEMENTO POR EDITAR"""
        formularioHora = HoraHorarioForm()
        formularioMaterias = MateriasHorarioForm(materias_grado=materias_grado)
        context = {
            'grado': grado,
            'vista': vista,
            'abierto':abierto,
            'horario':horarios_del_grado,
            #FORMULARIOS
            'formHora': formularioHora,
            'formMaterias': formularioMaterias,
        }
        return render(request, 'informacion/grados/horarios/ver_horario.html', context)

class EditarGradosHorarioHora(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk)
    
class EditarGradosHorarioLunes(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk)
    
class EditarGradosHorarioMartes(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk)
    
class EditarGradosHorarioMiercoles(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk)
    
class EditarGradosHorarioJueves(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk)


class EditarGradosHorarioViernes(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk)