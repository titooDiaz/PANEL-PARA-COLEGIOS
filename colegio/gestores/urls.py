from django.urls import path
from .views import CreateGestor, ViewUsersSettings, BoardGestores, CalendarioGestores, MensajesGestores, AjustesGestores, CreateAlumno, CreateProfesor, CreateGrados, CreateMaterias, CreateMateriasVer, CreateAcudiente, CreateAdmin, CreateHorarios, EditCortesHorarios, CreateCortes, EditCortes, CreateActividadTipo

urlpatterns = [
    #ver usuarios para modificar o ...
    path('board/', BoardGestores.as_view(), name='BoardGestores'),
    path('calendario/', CalendarioGestores.as_view(), name='CalendarioGestores'),
    path('mensajes/', MensajesGestores.as_view(), name='MensajesGestores'),
    path('personas/', ViewUsersSettings.as_view(), name='ViewUsersSettings'),
    path('ajustes/', AjustesGestores.as_view(), name='AjustesGestores'),

    #crear
    path('crear/profesores/', CreateProfesor.as_view(), name='CrearProfesor'),
    path('crear/gestores/', CreateGestor.as_view(), name='CrearGestor'),
    path('crear/alumnos/', CreateAlumno.as_view(), name='CrearAlumno'),
    path('crear/acudiente/', CreateAcudiente.as_view(), name='CrearAcudiente'),
    path('crear/admin/', CreateAdmin.as_view(), name='CrearAdmin'),
    path('crear/grados/', CreateGrados.as_view(), name='CrearGrado'),
    path('crear/materias/<int:pk>', CreateMaterias.as_view(), name='CrearMaterias'),
    
    # Horarios
    path('crear/horario/', CreateHorarios.as_view(), name='CrearHorarios'),
    path('crear/horario/cortes/', EditCortesHorarios.as_view(), name='CrearHorariosCortesGrados'),
    path('crear/horario/cortes/<int:pk>', CreateCortes.as_view(), name='CrearHorariosCortes'),
    path('crear/horario/cortes/<int:corte_pk>/<int:pk>', EditCortes.as_view(), name='EditHorariosCortes'),
    
    path('crear/materias/', CreateMateriasVer.as_view(), name='VerGradosMaterias'),
    
    # Actividades tipo
    path('crear/actividad/tipo/', CreateActividadTipo.as_view(), name='ActividadTipo'),
]