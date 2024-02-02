from django.shortcuts import render, get_object_or_404, redirect
from .models import Colegio
from django.views.generic import TemplateView, View
from .forms import ColegioForm

class GestionColegios(View):
    def get(self, request):
        colegios = Colegio.objects.all()
        form = ColegioForm()
        vista = 'gestor'
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
            'colegios': colegios
        }
        return render(request, 'colegios/CreateColegio.html', context)

    def post(self, request):
        form = ColegioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('Colegios')