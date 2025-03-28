from django.urls import path
from .views import AlumnoBoard, AlumnoCalendario, StudentMessages, StudentGrades, StudentPeople, ActividadesRespuestaView, SubjectsView

urlpatterns = [
    #vista estudiantes
    path('board/', AlumnoBoard.as_view(), name='BoardAlumno'),
    
    # es - Materias
    # en - Subjects
    path('materias/ver/<int:pk>', SubjectsView.as_view(), name='SubjectsView'),
    
    # es - Actividades
    # en - activities
    path('actividades/responder/<int:pk>', ActividadesRespuestaView.as_view(), name='ResponderActividades'),
    path('calendario/', AlumnoCalendario.as_view(), name='CalendarioAlumno'),
    
    # es - Mensajes
    # en - Messages
    path('mensajes/', StudentMessages.as_view(), name='MessagesStudent'),
    
    # es - Notas
    # en - Grades
    path('notas/', StudentGrades.as_view(), name='GradesStudent'),
    
    # es - Personas
    # en - People
    path('personas/', StudentPeople.as_view(), name='PeopleStudent'),
]
