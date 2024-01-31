from django.shortcuts import render
from django.views.generic import TemplateView, View  

class AcudienteBoard(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='calendario'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/admin/inicio.html', context)

