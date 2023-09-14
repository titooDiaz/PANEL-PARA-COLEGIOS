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
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/create_alumnos.html', context)
    


class AlumnoBoard(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='inicio'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/board.html', context)
    
class AlumnoCalendario(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='calendario'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/board.html', context)
    
class AlumnoMensajes(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='mensajes'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/board.html', context)
    
class AlumnoPersonas(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='personas'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/board.html', context)
    
class AlumnoNotas(View):
    def get(self, request, *args, **kwargs):
        vista = 'estudiante'
        abierto='notas'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/board.html', context)