from django.shortcuts import render, get_object_or_404, redirect
from .models import Grade, DailySchedule
from django.views.generic import TemplateView, View
from users.models import CustomUserStudent
from rest_framework import generics, permissions
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework.response import Response
from rest_framework import status

from .forms import HoraHorarioForm, MateriasHorarioForm, EditarVerNotasAlumnosForm


#Translate VerGrados
class SeeGrades(View):
    def get(self, request, *args, **kwargs):
        colegio = request.user.school.pk # get school 
        grados = Grade.objects.filter(school=colegio)
        print(grados)
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'grados': grados,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/grados/ver_grados.html', context)
    

"""VISTA INICIAL
VAMOS A USAR 'APIS', PARA NO SOBRECARGAR LA VISTA

LAS 'APIS' ESTAN ABAJO DE LA CLASE VerGradosHorario... 
PARA CADA MOVIMIENTO HYA UNA VISTA DEDICADA, QUE RETORNARA ESTA MISMA VISTA
         |
        \|/
"""

# EN ESTA VISTA PODREMOS VER TODA LA TABLA DE HORARIOS (POR DEFECTO VACIA) EN NUESTROS GRADOS.
#Translate VerGradosHorarios
class SeeGradesSchedules(View):
    def get(self, request, pk, *args, **kwargs):
        grado = Grade.objects.get(id=pk)
        horarios_del_grado = DailySchedule.objects.filter(grade=grado)
        vista = 'gestor'
        abierto='ajustes'

        #filtrar materias
        materias_grado = grado.subjects.all()
        """DEBEMOS CREAR UN FORMULARIO POR CADA ELEMENTO POR EDITAR"""
        formularioHora = HoraHorarioForm()
        formularioMaterias = MateriasHorarioForm(materias_grado=materias_grado)
        context = {
            'materias': materias_grado,
            'grado': grado,
            'vista': vista,
            'abierto':abierto,
            'horario':horarios_del_grado,
            #FORMULARIOS
            'formHora': formularioHora,
            'formMaterias': formularioMaterias,
        }
        return render(request, 'informacion/grados/horarios/ver_horario.html', context)
#                                  \__--> En la vista manejaremos la logica en la cual aparecera las materias correspondientes a cada grado. en caso de ser vacia mostraremos otra cosa :)


#Translate EditarGradosHorarioHora
class EditGradesScheduleHour(View):
    def post(self, request, pk_post, pk_vista, *args, **kwargs):
        instancia_modelo = get_object_or_404(DailySchedule, pk=pk_post)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk_vista)


#Translate EditarGradosHorarioMaterias
class EditGradesScheduleSubjects(View):
    def post(self, request, pk_post, pk_vista, *args, **kwargs):
        instancia_modelo = get_object_or_404(DailySchedule, pk=pk_post)
        valores_originales = { #GUARDAMOS LOS VALORES ORIGINALES PARA QUE NO SE ELIMINENA LA HORA DE HACER EL POST
            'monday': instancia_modelo.monday,
            'tuesday': instancia_modelo.tuesday,
            'wednesday': instancia_modelo.wednesday,
            'thursday': instancia_modelo.thursday,
            'friday': instancia_modelo.friday,
            'saturday': instancia_modelo.saturday,
        }
        formulario = MateriasHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            nuevos_valores = {
                'monday': formulario.cleaned_data['monday'],
                'tuesday': formulario.cleaned_data['tuesday'],
                'wednesday': formulario.cleaned_data['wednesday'],
                'thursday': formulario.cleaned_data['thursday'],
                'friday': formulario.cleaned_data['friday'],
                'saturday': formulario.cleaned_data['saturday'],
            }

            '''
            ENTIENDO QUE LA LOGICA PUEDA SER CONFUSA..
            LO UNICO QUE BUSCAMOS CON ESTAS CONDICIONES ES QUE SI UN VALOR NO FUE MODIFICADO NO SE VACIE, YA QUE
            DJANGO POR DEFECTO LSO VACIA SI NO LE ASIGNAMOS NINGUN VALOR, ENTONCES LO QUE ESTAMOS HACIENDO ES QUE 
            COMPARE EL VALOR ANTERIOR CON EL NUEVO, SI EL NUEVO VALOR NO ESTA VACIO (ES DECIR FUE MODIFICADO),
            Y EL VALOR ORIGINAL NO ES NONE (NO TENDRIA SENTIDO REMPLAZAR UN NONE CON UN NONE...)
            VAMOS A PONER EL NUEVO CAMPO CON EL CAMPO ANTIGUO
            '''
            if nuevos_valores['monday'] == None and valores_originales['monday'] != None:
                instancia_modelo.monday = valores_originales['monday']

            if nuevos_valores['tuesday'] == None and valores_originales['tuesday'] != None:
                instancia_modelo.tuesday = valores_originales['tuesday']

            if nuevos_valores['wednesday'] == None and valores_originales['wednesday'] != None:
                instancia_modelo.wednesday = valores_originales['wednesday']

            if nuevos_valores['thursday'] == None and valores_originales['thursday'] != None:
                instancia_modelo.thursday = valores_originales['thursday']

            if nuevos_valores['friday'] == None and valores_originales['friday'] != None:
                instancia_modelo.friday = valores_originales['friday']
                
            if nuevos_valores['saturday'] == None and valores_originales['saturday'] != None:
                instancia_modelo.saturday = valores_originales['saturday']

            formulario.save()

        return redirect('MirarGradoHorario', pk_vista)


#Translate EditarVerNotasAlumnos
class EditSeeRatingsStudents(View):
    def post(self, request, pk_post, pk_vista, *args, **kwargs):
        estudiante = CustomUserStudent.objects.get(pk=pk_post)
        formulario = EditarVerNotasAlumnosForm(request.POST, instance=estudiante)
        if formulario.is_valid():
            formulario.save()

        return redirect('VerEstudiantesGrado', pk_vista)


#Translate VerEstudiantesGrado
class SeeStudentsGrades(View):
    def get(self, request, pk, *args, **kwargs):
        grado = get_object_or_404(Grade, pk=pk)
        estudiantes = CustomUserStudent.objects.filter(grade=grado)
        print(grado)
        vista = 'gestor'
        abierto='ajustes'
        form = EditarVerNotasAlumnosForm()
        context = {
            'grado': grado,
            'estudiantes': estudiantes,
            'vista': vista,
            'abierto':abierto,
            'form': form,
        }
        return render(request, 'informacion/grados/ver_estudiantes.html', context)

class SendMessageView(generics.CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
