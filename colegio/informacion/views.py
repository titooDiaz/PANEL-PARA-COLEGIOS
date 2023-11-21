from django.shortcuts import render
from .models import Grado
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
