from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserAlumnoForm


class CreateAlumno(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm(request.POST)
        context = {
            'form': form
        }
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            alumno = form.save(commit=False)
            alumno.numero_documento = username
            alumno.save()
        else:
            print(form.errors)
        return redirect('CrearAlumno')
    def get(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm()
        vista = 'admin'
        context = {
            'form': form,
            'vista': vista,
        }
        return render(request, 'users/alumnos/create_alumnos.html', context)
    


class AlumnoBoard(View):
    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, 'users/alumnos/board.html', context)