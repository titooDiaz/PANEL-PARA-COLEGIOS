from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserManagerForm, CustomUserStudentForm, CustomUserTeachersForm, GradeForm, SubjectsForm, SchedulePartsForm, CustomUserGuardianForm, CustomUserAdminForm, CustomUserTeachers
from information.models import Grade, ScheduleParts, DailySchedule, ScheduleCourts, ActivitiesType
from django.contrib import messages
from users.models import CustomUserStudent
from .forms import ScheduleCourtsForm, ActivitiesTypeForm
from datetime import datetime, timedelta

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
        estudiantes = CustomUserStudent.objects.filter(grade_id=grado_id)
        return estudiantes
    except CustomUserStudent.DoesNotExist:
        return None
    
def obtener_profesores_por_colegio(grado_id):
    profesores = CustomUserTeachers.objects.filter(school_id=grado_id)
    return profesores
    
def obtener_grados_por_colegio(colegio_id):
    try:
        grados = Grade.objects.filter(school=colegio_id)
        if grados:
            print(Colores.CYAN + "[+] 'Grados' Of the 'Colegio' User:  " + str(grados) + Colores.RESET)
            return grados
        else:
            print(Colores.CYAN + "[+] 'Grados' Of the 'Colegio' User (This user not have 'Grados'):  " + Colores.RESET)
            return None
    except Grade.DoesNotExist:
        return None

###############################################################################################
class CreateAlumno(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserStudentForm(request.POST, request.FILES)
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
                form.instance.photo.save('profile.png', ContentFile(image_io.getvalue()))
            ######################################################
            
            #agregamos el resto del fomulario, usertname == documento 
            alumno = form.save(commit=False)
            alumno.school = request.user.school #El colegio del alumno va a ser el colegio del usuario en sesion SOLO SI SE CREA DESDE LA VISTA DEL GESTOR!
            alumno.document_number = username
                
            # Guardar el formulario para actualizar la instancia del modelo
            alumno.save()
            messages.success(request, "Alumno agregado correctamente!")
        else:
            mensaje = "¡Hubo un error al agregar el alumno!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        return redirect('CrearAlumno')
    def get(self, request, *args, **kwargs):
        colegio = request.user.school.pk
        grados = obtener_grados_por_colegio(colegio)#obtenemos unicamente los grados de este colegio
        
        form = CustomUserStudentForm(grado=grados)
        vista = 'gestor'
        abierto='personas'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        
        if not grados:
            return render(request, 'erros/error_no_grades.html', context)
        
        return render(request, 'users/alumnos/create_alumnos.html', context)

class CreateGestor(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserManagerForm(request.POST, request.FILES)
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
                form.instance.photo.save('profile.png', ContentFile(image_io.getvalue()))
            ######################################################
            gestor = form.save(commit=False)
            gestor.school = request.user.school
            gestor.document_number = username
            gestor.save()
            messages.success(request, "¡Gestor agregado correctamente!")
        else:
            mensaje = "¡Hubo un error al agregar el gestor!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        return redirect('CrearGestor')
    def get(self, request, *args, **kwargs):
        form = CustomUserManagerForm()
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
        form = CustomUserTeachersForm(request.POST, request.FILES)
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
                form.instance.photo.save('profile.png', ContentFile(image_io.getvalue()))
            ######################################################
            
            profesor = form.save(commit=False)
            profesor.document_number = username
            profesor.school = request.user.school
            profesor.save()
            messages.success(request, '¡Profesor agregado correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar el profesor!"
            messages_error.errores_formularios(form.errors, mensaje, request)
        return redirect('CrearProfesor')
    def get(self, request, *args, **kwargs):
        colegio = request.user.school.pk
        grados = obtener_grados_por_colegio(colegio)#obtenemos unicamente los grados de este colegio
        form = CustomUserTeachersForm(titular=grados)
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
        form = CustomUserAdminForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            profesor = form.save(commit=False)
            profesor.document_number = username
            profesor.save()
            messages.success(request, '¡Administrador agregado correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar el Administrador!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
            print(form.errors)
        return redirect('CrearAdmin')
    def get(self, request, *args, **kwargs):
        form = CustomUserAdminForm()
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
        form = CustomUserGuardianForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            profesor = form.save(commit=False)
            profesor.document_number = username
            profesor.save()
            messages.success(request, '¡Acudiente agregado correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar el Acudiente!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        return redirect('CrearAcudiente')
    def get(self, request, *args, **kwargs):
        estudiantes = request.user.school.pk
        vista = 'gestor'
        abierto='personas'
        try:
            form = CustomUserGuardianForm(estudiantes_colegio=estudiantes)
            context = {
                'form': form,
                'vista': vista,
                'abierto':abierto,
            }
        except:
            context = {
                'form': None,
                'vista': vista,
                'abierto':abierto,
            }
            return render(request, 'informacion/materias/error_no_estudiantes.html', context)
        return render(request, 'users/acudiente/create_acudiente.html', context)
    
class CreateGrados(View):
    def post(self, request, *args, **kwargs):
        colegio = request.user.school.pk
        form = GradeForm(request.POST, horario_partes=colegio)
        print(form.is_valid())
        if form.is_valid():
            try:
                grado = form.save(commit=False)
                
                ##############################
                # OBTENEMOS EL HORARIO SELECCIONADO POR EL FORMULARIO. PARAS PODER CREAR LA TABLA ED LOS HORARIOS DIARIOS
                horarios = form.cleaned_data.get('horario_partes')
                pk = horarios.pk
                horario = ScheduleParts.objects.get(id=pk)
                horas = horario.hours
                ##############################
                grado.school = request.user.school
                grado.author = request.user  # Asocia el autor con el usuario actual
                grado.save()

                for i in range(int(horas)):
                    DailySchedule.objects.create(grado=grado)
                    
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
        colegio = request.user.school.pk
        print(Colores.CYAN + "[+] 'Horario partes' Of the 'Colegio':  " + str(colegio) + Colores.RESET)
        form = GradeForm(horario_partes=colegio)
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/grados/create_grados.html', context)


def dividir_fechas_en_rangos(num_divisiones):
    # Ano actual
    ahora = datetime.now()
    ano_actual = ahora.year

    # (1 enero ano actual)
    fecha_inicio = datetime(ano_actual, 1, 1)

    # (ojala nunca cambien la fecha JAJAJ (31 diciembre ano actual))
    fecha_fin = datetime(ano_actual, 12, 31)

    # (duracion total)
    duracion_total = fecha_fin - fecha_inicio

    # Calcular la division del ano
    duracion_division = duracion_total / num_divisiones

    # Crear una lista de rangos
    rangos = []
    for i in range(num_divisiones):
        inicio = fecha_inicio + duracion_division * i
        fin = fecha_inicio + duracion_division * (i + 1) - timedelta(days=1)
        if i == num_divisiones - 1:  # Asegurar que el último rango termine el 31 de diciembre
            fin = fecha_fin
        
        rangos.append({
            "inicio": inicio.strftime('%Y-%m-%d'),
            "fin": fin.strftime('%Y-%m-%d')
        })

    return rangos

class CreateHorarios(View):
    def post(self, request, *args, **kwargs):
        form = SchedulePartsForm(request.POST)
        if form.is_valid():
            horario=form.save(commit=False)
            colegio=request.user.school
            horario.school=colegio #el horario del colegio va a ser el usuario en sesion en la vistas de admins!
            horario.author = request.user
            cortes = horario.school_cuts
            horario.save()
            horario_pk = horario.pk
            
            num_divisiones = cortes # cortes tiene el numero de cortes
            rangos = dividir_fechas_en_rangos(num_divisiones)

            for i, rango in enumerate(rangos):
                print(f"Rango {i + 1}: {rango['inicio']}   ---->   {rango['fin']}")
                ScheduleCourts.objects.create(horario=horario, corte_num=i+1, fecha_inicio=rango['inicio'], fecha_fin=rango['fin'])
                
            messages.success(request, '¡Horario agregado correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar el Horario!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        return redirect('CrearHorariosCortes', pk=horario_pk)
    
    def get(self, request, *args, **kwargs):
        form = SchedulePartsForm()
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
        form = SubjectsForm(request.POST, request.FILES)
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
                    form.instance.photo.save('picture.png', ContentFile(image_io.getvalue()))
                    print('saveee///')
                grado = Grade.objects.get(pk=pk)
                electiva_value = form.cleaned_data.get('electiva')
                
                # Limpia los campos relacionados con la electiva si no es True
                if not electiva_value:
                    materia.teacher_2 = None
                    materia.name_2 = ""
                    materia.description_2 = ""
                else:
                    alumnos1 = form.cleaned_data.get('alumnos1')
                    alumnos2 = form.cleaned_data.get('alumnos2')
                    materia.save()
                    materia.students_1.set(alumnos1)
                    materia.students_2.set(alumnos2)
                if materia.teacher_1 != materia.teacher_2 :
                    if (materia.teacher_1 != None and materia.teacher_2 != None and electiva_value) or (not electiva_value and materia.teacher_1 != None):
                        materia.save()
                        grado.subjects.add(materia)
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
        grado = Grade.objects.get(id=pk)
        estudiantes_grado = obtener_estudiantes_por_grado(pk)
        colegio=request.user.school
        profesores_grado = obtener_profesores_por_colegio(colegio)
        vista = 'gestor'
        abierto = 'ajustes'
        if estudiantes_grado:
            form = SubjectsForm(estudiantes_grado=estudiantes_grado, profesores=profesores_grado) #mandar alumnos del grado
            id_grado = pk
            grado = Grade.objects.get(pk=pk)
            materias = grado.subjects.all()
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
        grados = Grade.objects.filter(school=request.user.school)
        print(grados)
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'grados': grados,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/materias/ver_grados.html', context)
    
class EditCortesHorarios(View):
    def get(self, request, *args, **kwargs):
        horario = ScheduleParts.objects.filter(school=request.user.school)
        print(horario)
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'horarios': horario,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'informacion/horarios/list_horarios_cortes.html', context)
    
class CreateCortes(View):
    def get(self, request, pk, *args, **kwargs):
        form = ScheduleCourtsForm()
        horario_id = pk
        cortes = ScheduleCourts.objects.filter(schedule=horario_id)
        vista = 'gestor'
        abierto='ajustes'
        context = {
            'horario_pk': horario_id,
            'cortes': cortes,
            'vista': vista,
            'abierto':abierto,
            'form': form,
        }
        return render(request, 'informacion/horarios/edit_cortes.html', context)


def verificar_fecha(horario_pk, corte_pk):
    corte = ScheduleCourts.objects.get(id=corte_pk)
    if not(corte.start_date < corte.end_date):
        return False
    
    cortes = ScheduleCourts.objects.filter(schedule=horario_pk)
    fechas = [(i.start_date, i.end_date) for i in cortes]
    
    for i, (inicio1, fin1) in enumerate(fechas):
        for j, (inicio2, fin2) in enumerate(fechas):
            if i != j:
                if not (fin1 < inicio2 or fin2 < inicio1):
                    return False
                if not(fin1 > inicio1 or fin2 > inicio2):
                    return False
    return True


class EditCortes(View):
    def post(self, request, corte_pk, pk, *args, **kwargs):
        horario = get_object_or_404(ScheduleCourts, id=corte_pk)
        
        # Guardar las fechas originales
        fecha_inicio_original = horario.start_date
        fecha_fin_original = horario.end_date

        print(fecha_fin_original, fecha_inicio_original)  # Para debug
        form = ScheduleCourtsForm(request.POST, instance=horario)

        if form.is_valid():
            # Obtener valores del Formulario
            cleaned_data = form.cleaned_data

            # Guardar temporalmente las nuevas fechas
            nueva_fecha_inicio = cleaned_data.get('start_date')
            nueva_fecha_fin = cleaned_data.get('end_date')

            form.save()  # Guardar los datos temporalmente en la instancia de horario

            # Verificar las fechas usando los datos del formulario
            if verificar_fecha(pk, corte_pk):
                messages.success(request, '¡Editaste el corte correctamente!')
            else:
                # Revertir las fechas al valor original
                horario.start_date = fecha_inicio_original
                horario.end_date = fecha_fin_original
                horario.save()  # Guardar los cambios revertidos en la base de datos
                
                messages.error(
                    request,
                    f'¡Las fechas están intersectadas o cometiste algún error: ({nueva_fecha_inicio}) con ({nueva_fecha_fin}), revisa tus registros!'
                )
        else:
            mensaje = "¡Hubo un error al editar el corte!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        
        return redirect('CrearHorariosCortes', pk=pk)
    
    
class CreateActividadTipo(View):
    def post(self, request, *args, **kwargs):
        form = ActivitiesTypeForm(request.POST)
        if form.is_valid():
            tipo_actividad = form.save(commit=False)
            tipo_actividad.school = request.user.school
            tipo_actividad.author = request.user
            tipo_actividad.save()
                
            messages.success(request, '¡Actividad agregada correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar este tipo de actividad!"
            messages_error.errores_formularios(form.errors, mensaje, request)
            print(form.errors)
        return redirect('ActividadTipo')
    
    def get(self, request, *args, **kwargs):
        form = ActivitiesTypeForm()
        vista = 'gestor'
        abierto='ajustes'
        actividades_creadas = ActivitiesType.objects.filter(school = request.user.school)
        context = {
            'vista': vista,
            'abierto':abierto,
            'form': form,
            'actividades': actividades_creadas,
        }
        return render(request, 'informacion/actividades/actividades.html', context)