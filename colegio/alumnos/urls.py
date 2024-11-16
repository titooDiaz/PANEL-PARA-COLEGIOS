from django.urls import path
from .views import AlumnoBoard, AlumnoCalendario, StudentMessages, AlumnoNotas, StudentPeople, ActividadesRespuestaView

urlpatterns = [
    #vista estudiantes
    path('board/', AlumnoBoard.as_view(), name='BoardAlumno'),
    
    # es - Actividades
    # en - activities
    path('actividades/responder/<int:pk>', ActividadesRespuestaView.as_view(), name='ResponderActividades'),
    path('calendario/', AlumnoCalendario.as_view(), name='CalendarioAlumno'),
    
    # es - Mensajes
    # en - Messages
    path('mensajes/', StudentMessages.as_view(), name='MessagesStudent'),
    
    # es - Notas
    # en - Grades
    path('notas/', AlumnoNotas.as_view(), name='NotasAlumno'),
    
    # es - Personas
    # en - People
    path('personas/', StudentPeople.as_view(), name='PeopleStudent'),
]
