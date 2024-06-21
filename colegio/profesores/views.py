from django.shortcuts import render
from django.views.generic import TemplateView, View

class BoardProfesores(View):
    def get(self, request, *args, **kwargs):
        vista = 'gestor'
        abierto='inicio'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/profesores/inicio.html', context)
