from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserGestorForm, CustomUserAlumnoForm, CustomUserProfesoresForm, GradoForm, MateriasForm
from informacion.models import Grado


class CreateAlumno(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm(request.POST)
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
        vista = 'gestor'
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/alumnos/create_alumnos.html', context)

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
    
class BoardGestores(View):
    def get(self, request, *args, **kwargs):
        vista = 'gestor'
        abierto='inicio'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/gestores/personas_views.html', context)
    
class CalendarioGestores(View):
    def get(self, request, *args, **kwargs):
        vista = 'gestor'
        abierto='calendario'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/gestores/personas_views.html', context)

class MensajesGestores(View):
    def get(self, request, *args, **kwargs):
        vista = 'gestor'
        abierto='mensajes'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/gestores/personas_views.html', context)

class AjustesGestores(View):
    def get(self, request, *args, **kwargs):
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/view_informacion.html', context)
    
class CreateProfesor(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserProfesoresForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            profesor = form.save(commit=False)
            profesor.numero_documento = username
            profesor.save()
        else:
            print(form.errors)
        return redirect('CrearProfesor')
    def get(self, request, *args, **kwargs):
        form = CustomUserProfesoresForm()
        vista = 'gestor'
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/profesores/create_profesores.html', context)
    
class CreateAdmin(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserProfesoresForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            profesor = form.save(commit=False)
            profesor.numero_documento = username
            profesor.save()
        else:
            print(form.errors)
        return redirect('CrearProfesor')
    def get(self, request, *args, **kwargs):
        form = CustomUserProfesoresForm()
        vista = 'gestor'
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/admin/create_admin.html', context)
    
class CreateAcudiente(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserProfesoresForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            profesor = form.save(commit=False)
            profesor.numero_documento = username
            profesor.save()
        else:
            print(form.errors)
        return redirect('CrearProfesor')
    def get(self, request, *args, **kwargs):
        form = CustomUserProfesoresForm()
        vista = 'gestor'
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'users/acudiente/create_acudiente.html', context)
    
class CreateGrados(View):
    def post(self, request, *args, **kwargs):
        form = GradoForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            grado = form.save(commit=False)
            grado.author = request.user  # Asocia el autor con el usuario actual
            grado.save()
        else:
            print(form.errors)
        return redirect('CrearGrado')
    def get(self, request, *args, **kwargs):
        form = GradoForm()
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/grados/create_grados.html', context)

    
class CreateMaterias(View):
    def post(self, request, pk, *args, **kwargs):
        form = MateriasForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            grado = Grado.objects.get(pk=pk)  # Obtén el grado desde la URL
            materia.author = request.user
            materia.save()
            grado.materias.add(materia)
            return redirect('CrearMaterias', pk=pk)  # Redirige a la misma vista
        return redirect('CrearMaterias', pk=pk)  # Si el formulario no es válido

    def get(self, request, *args, **kwargs):
        form = MateriasForm()
        vista = 'gestor'
        abierto = 'ajustes'
        context = {
            'form': form,
            'vista': vista,
            'abierto': abierto,
        }
        return render(request, 'informacion/materias/create_materias.html', context)

class CreateMateriasVer(View):
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
        return render(request, 'informacion/materias/ver_grados.html', context)