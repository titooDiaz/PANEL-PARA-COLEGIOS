from django.urls import path
from .views import CreateGestor, ViewUsersSettings, BoardGestores, CalendarioGestores, MensajesGestores, AjustesGestores, CreateAlumno, CreateProfesor, CreateGrados, CreateMaterias, CreateMateriasVer, CreateAcudiente, CreateAdmin, CreateHorarios

urlpatterns = [
    #ver usuarios para modificar o ...
    path('board/', BoardGestores.as_view(), name='BoardGestores'),
    path('calendario/', CalendarioGestores.as_view(), name='CalendarioGestores'),
    path('mensajes/', MensajesGestores.as_view(), name='MensajesGestores'),
    path('personas/', ViewUsersSettings.as_view(), name='ViewUsersSettings'),
    path('ajustes/', AjustesGestores.as_view(), name='AjustesGestores'),

    path('crear/profesores', CreateProfesor.as_view(), name='CrearProfesor'),
    path('crear/gestores/', CreateGestor.as_view(), name='CrearGestor'),
    path('crear/alumnos', CreateAlumno.as_view(), name='CrearAlumno'),
    path('crear/acudiente', CreateAcudiente.as_view(), name='CrearAcudiente'),
    path('crear/admin', CreateAdmin.as_view(), name='CrearAdmin'),
    path('crear/grados/', CreateGrados.as_view(), name='CrearGrado'),
    path('crear/materias/<int:pk>', CreateMaterias.as_view(), name='CrearMaterias'),
    path('crear/horario', CreateHorarios.as_view(), name='CrearHorarios'),
    path('crear/materias', CreateMateriasVer.as_view(), name='VerGradosMaterias'),
]