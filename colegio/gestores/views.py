from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserGestorForm, CustomUserAlumnoForm, CustomUserProfesoresForm, GradoForm, MateriasForm, Horarios_PartesForm, CustomUserAcudienteForm, CustomUserAdministradorForm
from informacion.models import Grado,Horarios_Partes, HorarioDiario, HorarioCortes
from django.contrib import messages
from users.models import CustomUserAlumno

#colores para consola
from colores import Colores

#trabaja con imagenes y espacios en la memoria
import io
from PIL import Image
from django.core.files.base import ContentFile

## MENSAJES DE ERRORES ##
from message_error import messages_error



############################## RECORTE DE IMAGENES ##################################################
def recorte_imagenes(cords, foto):
    cords = cords.split(',')
    coordenadas_recorte = (
        int(cords[0]),
        int(cords[1]),
        int(cords[0]) + int(cords[2]),
        int(cords[1]) + int(cords[3])
    )

    imagen_original = Image.open(foto)
    imagen_recortada = imagen_original.crop(coordenadas_recorte)

    # Crear un objeto de archivo en memoria y guardar la imagen recortada en él
    image_io = io.BytesIO()
    imagen_recortada.save(image_io, format='PNG')#GUARDAMOS LA NUEVA IMAGEN EN FORMATO PNG EN LA VARIABLE 'image_io'
    return image_io
################################ FIN RECORTE IMAGENES ##################################################




#################################CONSULTAS####################################################

def obtener_estudiantes_por_grado(grado_id):
    try:
        estudiantes = CustomUserAlumno.objects.filter(grado_id=grado_id)
        return estudiantes
    except CustomUserAlumno.DoesNotExist:
        return None
    
def obtener_grados_por_colegio(colegio_id):
    try:
        grados = Grado.objects.filter(colegio=colegio_id)
        print(Colores.CYAN + "--->'Grados' Of the 'Colegio' User:  " + str(grados) + Colores.RESET)
        return grados
    except Grado.DoesNotExist:
        return None

###############################################################################################
class CreateAlumno(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            
            ##################### FOTO #########################
            foto = form.cleaned_data.get('foto')
            if foto != 'alumnos/profile.png':
                cords = form['cords'].value()
                cords= cords.split(':')
                cords = cords[0]
                
                image_io = recorte_imagenes(cords, foto)
                # Asignar el objeto de archivo al campo 'foto'
                form.instance.foto.save('profile.png', ContentFile(image_io.getvalue()))
            ######################################################
            
            #agregamos el resto del fomulario, usertname == documento 
            alumno = form.save(commit=False)
            alumno.colegio = request.user.colegio #El colegio del alumno va a ser el colegio del usuario en sesion SOLO SI SE CREA DESDE LA VISTA DEL GESTOR!
            alumno.numero_documento = username
                
            # Guardar el formulario para actualizar la instancia del modelo
            alumno.save()
            messages.success(request, "Alumno agregado correctamente!")
        else:
            mensaje = "¡Hubo un error al agregar el alumno!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        return redirect('CrearAlumno')
    def get(self, request, *args, **kwargs):
        colegio = request.user.colegio.pk
        grados = obtener_grados_por_colegio(colegio)#obtenemos unicamente los grados de este colegio
        form = CustomUserAlumnoForm(grado=grados)
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
        form = CustomUserGestorForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            ##################### FOTO #########################
            foto = form.cleaned_data.get('foto')
            print(foto,"hola")
            if foto != 'gestores/profile.png' : #diferente de la imagen por defecto...
                cords = form['cords'].value()
                cords= cords.split(':')
                cords = cords[0]
                
                image_io = recorte_imagenes(cords, foto)
                # Asignar el objeto de archivo al campo 'foto'
                form.instance.foto.save('profile.png', ContentFile(image_io.getvalue()))
            ######################################################
            gestor = form.save(commit=False)
            gestor.colegio = request.user.colegio
            gestor.numero_documento = username
            gestor.save()
            messages.success(request, "¡Gestor agregado correctamente!")
        else:
            mensaje = "¡Hubo un error al agregar el gestor!"
            messages_error.errores_formularios(form.errors, mensaje, request)
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
        form = CustomUserProfesoresForm(request.POST, request.FILES)
        print(form.is_valid(),"holaaaa")
        if form.is_valid():
            username = form.cleaned_data['username']
            
            ##################### FOTO #########################
            foto = form.cleaned_data.get('foto')
            print(foto,"hola")
            if foto != 'profesores/profile.png' : #diferente de la imagen por defecto...
                cords = form['cords'].value()
                cords= cords.split(':')
                cords = cords[0]
                
                image_io = recorte_imagenes(cords, foto)
                # Asignar el objeto de archivo al campo 'foto'
                form.instance.foto.save('profile.png', ContentFile(image_io.getvalue()))
            ######################################################
            
            profesor = form.save(commit=False)
            profesor.numero_documento = username
            profesor.colegio = request.user.colegio
            profesor.save()
            messages.success(request, '¡Profesor agregado correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar el profesor!"
            messages_error.errores_formularios(form.errors, mensaje, request)
        return redirect('CrearProfesor')
    def get(self, request, *args, **kwargs):
        colegio = request.user.colegio.pk
        grados = obtener_grados_por_colegio(colegio)#obtenemos unicamente los grados de este colegio
        form = CustomUserProfesoresForm(titular=grados)
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
            mensaje = "¡Hubo un error al agregar el Administrador!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
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
            mensaje = "¡Hubo un error al agregar el Acudiente!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        return redirect('CrearAcudiente')
    def get(self, request, *args, **kwargs):
        estudiantes = request.user.colegio.pk
        form = CustomUserAcudienteForm(estudiantes_colegio=estudiantes)
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
            try:
                grado = form.save(commit=False)
                
                ##############################
                # OBTENEMOS EL HORARIO SELECCIONADO POR EL FORMULARIO. PARAS PODER CREAR LA TABLA ED LOS HORARIOS DIARIOS
                horarios = form.cleaned_data.get('horario_partes')
                pk = horarios.pk
                horario = Horarios_Partes.objects.get(id=pk)
                horas = horario.horas
                ##############################
                grado.colegio = request.user.colegio
                grado.author = request.user  # Asocia el autor con el usuario actual
                grado.save()

                for i in range(int(horas)):
                    HorarioDiario.objects.create(grado=grado)
                    
                messages.success(request, '¡Grado creado correctamente!')
            except:
                mensaje = "¡No olvides seleccionar un horario para tu grado!"
                messages_error.errores_formularios(form.errors, mensaje, request)
        else:
            mensaje = "¡Hubo un error al agregar el Grado!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
            print(form.errors)
        return redirect('CrearGrado')
    def get(self, request, *args, **kwargs):
        colegio = request.user.colegio.pk
        print(Colores.CYAN + "--->'Horario partes' Of the 'Colegio':  " + str(colegio) + Colores.RESET)
        form = GradoForm(horario_partes=colegio)
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
            colegio=request.user.colegio
            horario.colegio=colegio #el horario del colegio va a ser el usuario en sesion en la vistas de admins!
            horario.author = request.user
            cortes = horario.cortes
            horario.save()
            
            for i in range(int(cortes)):
                HorarioCortes.objects.create(colegio=colegio, corte_num=i+1)
                
            messages.success(request, '¡Horario agregado correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar el Horario!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
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
        form = MateriasForm(request.POST, request.FILES)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.author = request.user
            try:
                ###############################
                foto = form.cleaned_data.get('picture1')
                print(foto,"hola")
                if foto != 'materias/picture.png' : #diferente de la imagen por defecto...
                    cords = form['cords'].value()
                    cords= cords.split(':')
                    cords = cords[0]
                    
                    image_io = recorte_imagenes(cords, foto)
                    # Asignar el objeto de archivo al campo 'picture1'
                    form.instance.picture1.save('picture.png', ContentFile(image_io.getvalue()))
                    print('saveee///')
                grado = Grado.objects.get(pk=pk)
                electiva_value = form.cleaned_data.get('electiva')
                
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
                if materia.profe1 != materia.profe2 :
                    if (materia.profe1 != None and materia.profe2 != None and electiva_value) or (not electiva_value and materia.profe1 != None):
                        materia.save()
                        grado.materias.add(materia)
                        messages.success(request, '¡Materia creada correctamente!')
                    else:
                        mensaje = "¡No Dejes profesores vacios!"
                        messages_error.errores_formularios(form.errors, mensaje, request)
                else:
                    mensaje = "¡No selecciones profesores iguales para la electiva!"
                    messages_error.errores_formularios(form.errors, mensaje, request) 
            except Exception as e:
                print(e)
                mensaje = "¡Hubo un error al agregar esta materia, NO dejes campos vacios!"
                print(form.errors, "...")
                messages_error.errores_formularios(form.errors, mensaje, request) 
        else:
            mensaje = "¡Hubo un error al agregar esta materia!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)

        return redirect('CrearMaterias', pk=pk)

    def get(self, request, pk, *args, **kwargs):
        grado = Grado.objects.get(id=pk)
        estudiantes_grado = obtener_estudiantes_por_grado(pk)
        vista = 'gestor'
        abierto = 'ajustes'
        if estudiantes_grado:
            form = MateriasForm(estudiantes_grado=estudiantes_grado) #mandar alumnos del grado
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
        else:
            #en caso de ser vacio
            context= {
                'vista': vista,
                'abierto': abierto,
            }
            return render(request, 'informacion/materias/error_no_estudiantes.html', context)

class CreateMateriasVer(View):
    def get(self, request, *args, **kwargs):
        grados = Grado.objects.filter(colegio=request.user.colegio)
        print(grados)
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'grados': grados,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/materias/ver_grados.html', context)