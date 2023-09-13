from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserAlumnoForm


class CreateAlumno(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
        return render(request, 'users/alumnos/create_alumnos.html', context)
    def get(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm()
        context = {
            'form': form
        }
        return render(request, 'users/alumnos/create_alumnos.html', context)
    


class AlumnoBoard(View):
    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, 'users/alumnos/board.html', context)