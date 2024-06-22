from django.shortcuts import render
from django.views.generic import TemplateView, View
from informacion.models import Materias, Grado

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
