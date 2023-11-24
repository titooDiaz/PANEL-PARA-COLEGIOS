from django.shortcuts import render
from .models import Grado, HorarioDiario
from django.views.generic import TemplateView, View

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
        context = {
            'grado': grado,
            'vista': vista,
            'abierto':abierto,
            'horario':horarios_del_grado,
        }
        return render(request, 'informacion/grados/horarios/ver_horario.html', context)
