from django.urls import path
from .views import CreateAlumno, AlumnoBoard

urlpatterns = [
    path('crear/', CreateAlumno.as_view(), name='CrearAlumno'),
    path('board/', AlumnoBoard.as_view(), name='BoardAlumno'),
]
