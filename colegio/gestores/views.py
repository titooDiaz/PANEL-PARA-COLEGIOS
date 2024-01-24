from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserGestorForm, CustomUserAlumnoForm, CustomUserProfesoresForm, GradoForm, MateriasForm, Horarios_PartesForm, CustomUserAcudienteForm, CustomUserAdministradorForm
from informacion.models import Grado,Horarios_Partes, HorarioDiario
from django.contrib import messages

from users.models import CustomUserAlumno

def obtener_estudiantes_por_grado(grado_id):
    try:
        estudiantes = CustomUserAlumno.objects.filter(grado_id=grado_id)
        return estudiantes
    except CustomUserAlumno.DoesNotExist:
        return None

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
            messages.success(request, '¡Profesor agregado correctamente!')
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
        form = CustomUserAdministradorForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            profesor = form.save(commit=False)
            profesor.numero_documento = username
            profesor.save()
            messages.success(request, '¡Administrador agregado correctamente!')
        else:
            print(form.errors)
        return redirect('CrearAdmin')
    def get(self, request, *args, **kwargs):
        form = CustomUserAdministradorForm()
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
        form = CustomUserAcudienteForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            profesor = form.save(commit=False)
            profesor.numero_documento = username
            profesor.save()
            messages.success(request, '¡Acudiente agregado correctamente!')
        else:
            print(form.errors)
        return redirect('CrearAcudiente')
    def get(self, request, *args, **kwargs):
        form = CustomUserAcudienteForm()
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
            horarios = form.cleaned_data.get('horario_partes')
            palabras = str(horarios).split()
            horarios = ' '.join(palabras[2:])
            horario = Horarios_Partes.objects.get(titulo=horarios)
            horas = horario.horas
            
            grado.author = request.user  # Asocia el autor con el usuario actual
            grado.save()

            for i in range(int(horas)):
                HorarioDiario.objects.create(grado=grado)
                
            messages.success(request, '¡Grado creado correctamente!')
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


class CreateHorarios(View):
    def post(self, request, *args, **kwargs):
        form = Horarios_PartesForm(request.POST)
        if form.is_valid():
            horario=form.save(commit=False)
            horario.author = request.user
            horario.save()
            messages.success(request, '¡Horario agregado correctamente!')
        return redirect('CrearHorarios')
    
    def get(self, request, *args, **kwargs):
        form = Horarios_PartesForm()
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'vista': vista,
            'abierto':abierto,
            'form': form,
        }
        return render(request, 'informacion/horarios/create_horarios.html', context)
    
class CreateMaterias(View):
    def post(self, request, pk, *args, **kwargs):
        form = MateriasForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            grado = Grado.objects.get(pk=pk)
            materia.author = request.user
            electiva_value = form.cleaned_data.get('electiva')
            messages.success(request, '¡Materia creada correctamente!')
            
            # Limpia los campos relacionados con la electiva si no es True
            if not electiva_value:
                materia.profe2 = None
                materia.titulo2 = ""
                materia.descripcion2 = ""
            else:
                alumnos1 = form.cleaned_data.get('alumnos1')
                alumnos2 = form.cleaned_data.get('alumnos2')
                materia.save()
                materia.alumnos1.set(alumnos1)
                materia.alumnos2.set(alumnos2)
            
            materia.save()
            grado.materias.add(materia)

            return redirect('CrearMaterias', pk=pk)
        return redirect('CrearMaterias', pk=pk)

    def get(self, request, pk, *args, **kwargs):
        grado = Grado.objects.get(id=pk)
        estudiantes_grado = obtener_estudiantes_por_grado(pk)
        #form = MateriasForm(initial={'alumnos1': estudiantes_grado, 'alumnos2': estudiantes_grado})
        form = MateriasForm(estudiantes_grado=estudiantes_grado) #mandar alumnos del grado
        vista = 'gestor'
        abierto = 'ajustes'
        id_grado = pk
        grado = Grado.objects.get(pk=pk)
        materias = grado.materias.all()
        context = {
            'id_grado': id_grado,
            'form': form,
            'vista': vista,
            'abierto': abierto,
            'materias': materias,
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