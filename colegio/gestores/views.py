from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserGestorForm


class CreateGestor(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserGestorForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            gestor = form.save(commit=False)
            gestor.numero_documento = username
            gestor.save()
        else:
            print(form.errors)
        return redirect('CrearGestor')
    def get(self, request, *args, **kwargs):
        form = CustomUserGestorForm()
        vista = 'gestor'
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/gestores/create_gestores.html', context)
    
class ViewUsersSettings(View):
    def get(self, request, *args, **kwargs):
        vista = 'gestor'
        abierto='personas'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/gestores/personas_views.html', context)