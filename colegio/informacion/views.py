from django.shortcuts import render, get_object_or_404, redirect
from .models import Grado, HorarioDiario
from django.views.generic import TemplateView, View

from .forms import HoraHorarioForm, MateriasHorarioForm

class VerGrados(View):
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
        return render(request, 'informacion/grados/ver_grados.html', context)
    

"""VISTA INICIAL
VAMOS A USAR 'APIS', PARA NO SOBRECARGAR LA VISTA

LAS 'APIS' ESTAN ABAJO DE LA CLASE VerGradosHorario... 
PARA CADA MOVIMIENTO HYA UNA VISTA DEDICADA, QUE RETORNARA ESTA MISMA VISTA
         |
        \|/
"""
class VerGradosHorario(View):
    def get(self, request, pk, *args, **kwargs):
        grado = Grado.objects.get(id=pk)
        horarios_del_grado = HorarioDiario.objects.filter(grado=grado)
        vista = 'gestor'
        abierto='ajustes'

        #filtrar materias
        materias_grado = grado.materias.all()
        """DEBEMOS CREAR UN FORMULARIO POR CADA ELEMENTO POR EDITAR"""
        formularioHora = HoraHorarioForm()
        formularioMaterias = MateriasHorarioForm(materias_grado=materias_grado)
        context = {
            'grado': grado,
            'vista': vista,
            'abierto':abierto,
            'horario':horarios_del_grado,
            #FORMULARIOS
            'formHora': formularioHora,
            'formMaterias': formularioMaterias,
        }
        return render(request, 'informacion/grados/horarios/ver_horario.html', context)

class EditarGradosHorarioHora(View):
    def post(self, request, pk_post, pk_vista, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk_post)
        formulario = HoraHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            formulario.save()

        return redirect('MirarGradoHorario', pk_vista)
    
class EditarGradosHorarioMaterias(View):
    def post(self, request, pk_post, pk_vista, *args, **kwargs):
        instancia_modelo = get_object_or_404(HorarioDiario, pk=pk_post)
        valores_originales = { #evitar que se eliminen
            'lunes': instancia_modelo.lunes,
            'martes': instancia_modelo.martes,
            'miercoles': instancia_modelo.miercoles,
            'jueves': instancia_modelo.jueves,
            'viernes': instancia_modelo.viernes,
        }
        formulario = MateriasHorarioForm(request.POST, instance=instancia_modelo) #EDITAR EL CAMPO YA EXISTENTE...
        if formulario.is_valid():
            nuevos_valores = {
                'lunes': formulario.cleaned_data['lunes'],
                'martes': formulario.cleaned_data['martes'],
                'miercoles': formulario.cleaned_data['miercoles'],
                'jueves': formulario.cleaned_data['jueves'],
                'viernes': formulario.cleaned_data['viernes'],
            }

            '''
            ENTIENDO QUE LA LOGICA PUEDA SER CONFUSA..
            LO UNICO QUE BUSCAMOS CON ESTAS CONDICIONES ES QUE SI UN VALOR NO FUE MODIFICADO NO SE VACIE, YA QUE
            DJANGO POR DEFECTO LSO VACIA SI NO LE ASIGNAMOS NINGUN VALOR, ENTONCES LO QUE ESTAMOS HACIENDO ES QUE 
            COMPARE EL VALOR ANTERIOR CON EL NUEVO, SI EL NUEVO VALOR NO ESTA VACIO (ES DECIR FUE MODIFICADO),
            Y EL VALOR ORIGINAL NO ES NONE (NO TENDRIA SENTIDO REMPLAZAR UN NONE CON UN NONE...)
            VAMOS A PONER EL NUEVO CAMPO CON EL CAMPO ANTIGUO
            '''
            if nuevos_valores['lunes'] == None and valores_originales['lunes'] != None:
                instancia_modelo.lunes = valores_originales['lunes']

            if nuevos_valores['martes'] == None and valores_originales['martes'] != None:
                instancia_modelo.martes = valores_originales['martes']

            if nuevos_valores['miercoles'] == None and valores_originales['miercoles'] != None:
                instancia_modelo.miercoles = valores_originales['miercoles']

            if nuevos_valores['jueves'] == None and valores_originales['jueves'] != None:
                instancia_modelo.jueves = valores_originales['jueves']

            if nuevos_valores['viernes'] == None and valores_originales['viernes'] != None:
                instancia_modelo.viernes = valores_originales['viernes']

            formulario.save()

        return redirect('MirarGradoHorario', pk_vista)