from django.urls import path
from .views import CreateAlumno, AlumnoBoard, AlumnoCalendario, AlumnoMensajes, AlumnoNotas, AlumnoPersonas

urlpatterns = [
    path('crear/', CreateAlumno.as_view(), name='CrearAlumno'),

    #vista estudiantes
    path('board/', AlumnoBoard.as_view(), name='BoardAlumno'),
    path('calendario/', AlumnoCalendario.as_view(), name='CalendarioAlumno'),
    path('mensajes/', AlumnoMensajes.as_view(), name='MensajesAlumno'),
    path('notas/', AlumnoNotas.as_view(), name='NotasAlumno'),
    path('personas/', AlumnoPersonas.as_view(), name='PersonasAlumno'),
]
