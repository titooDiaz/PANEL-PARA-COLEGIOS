from django.urls import path
from .views import AlumnoBoard, AlumnoCalendario, AlumnoMensajes, AlumnoNotas, AlumnoPersonas

urlpatterns = [

    #vista estudiantes
    path('board/', AlumnoBoard.as_view(), name='BoardAlumno'),
    path('calendario/', AlumnoCalendario.as_view(), name='CalendarioAlumno'),
    path('mensajes/', AlumnoMensajes.as_view(), name='MensajesAlumno'),
    path('notas/', AlumnoNotas.as_view(), name='NotasAlumno'),
    path('personas/', AlumnoPersonas.as_view(), name='PersonasAlumno'),
]
