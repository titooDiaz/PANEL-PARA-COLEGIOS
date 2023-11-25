from django.shortcuts import render, get_object_or_404, redirect
from .models import Grado, HorarioDiario
from django.views.generic import TemplateView, View

from .forms import HoraHorarioForm

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
    
class VerGradosHorario(View):
    def get(self, request, pk, *args, **kwargs):
        grado = Grado.objects.get(id=pk)
        horarios_del_grado = HorarioDiario.objects.filter(grado=grado)
        vista = 'gestor'
        abierto='ajustes'
        formulario = HoraHorarioForm()
        context = {
            'grado': grado,
            'vista': vista,
            'abierto':abierto,
            'horario':horarios_del_grado,
            'form': formulario,
        }
        return render(request, 'informacion/grados/horarios/ver_horario.html', context)

class EditarGradosHorarioHora(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo)
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario')
    
class EditarGradosHorarioLunes(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo)
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario')
    
class EditarGradosHorarioMartes(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo)
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario')
    
class EditarGradosHorarioMiercoles(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo)
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario')
    
class EditarGradosHorarioJueves(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo)
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario')


class EditarGradosHorarioViernes(View):
    def post(self, request, pk, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo)
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario')