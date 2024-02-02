from django.shortcuts import render, get_object_or_404, redirect
from .models import Colegio
from django.views.generic import TemplateView, View
from .forms import ColegioForm

class GestionColegios(View):
    def get(self, request):
        colegios = Colegio.objects.all()
        form = ColegioForm()
        return render(request, self.template_name, {'colegios': colegios, 'form': form})

    def post(self, request):
        form = ColegioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nombre_de_la_url_de_la_vista')  # Reemplaza 'nombre_de_la_url_de_la_vista' con el nombre de la URL a la que deseas redirigir después de agregar un colegio
        else:
            colegios = Colegio.objects.all()
            return render(request, self.template_name, {'colegios': colegios, 'form': form})