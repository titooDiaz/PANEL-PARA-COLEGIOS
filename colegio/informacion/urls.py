from django.urls import path
from .views import VerGrados, VerGradosHorario, VerEstudiantesGrado

#'APIS'
from .views import EditarGradosHorarioHora, EditarGradosHorarioMaterias, EditarVerNotasAlumnos

urlpatterns = [    
    #editar
    path('grados/mirar/', VerGrados.as_view(), name='MirarGrados'),

    #MIRAR ESTUDIANTES
    path('grados/mirar/estudiantes/<int:pk>/', VerEstudiantesGrado.as_view(), name='VerEstudiantesGrado'),
    #MIRAR HORARIOS
    path('grados/mirar/horario/<int:pk>/', VerGradosHorario.as_view(), name='MirarGradoHorario'),
    #'APIS' PARA EL FORMULARIO DE HORARIOS
    path('grados/editar/horario/hora/<int:pk_post>/<int:pk_vista>/', EditarGradosHorarioHora.as_view(), name='EditarHorarioHora'),
    path('grados/editar/horario/materias/<int:pk_post>/<int:pk_vista>/', EditarGradosHorarioMaterias.as_view(), name='EditarHorarioMaterias'),
    #'APIS' PARA EDITAR VER NOTAS DE ALUMNOS #pk post = alumno
    path('grados/editar/ver/Notas/<int:pk_post>/<int:pk_vista>/', EditarVerNotasAlumnos.as_view(), name='EditarVerNotasAlumnos'),
]