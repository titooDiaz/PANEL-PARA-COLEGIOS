from django.urls import path
from .views import SeeGrades, SeeGradesSchedules, SeeStudentsGrades

#'APIS'
from .views import EditGradesScheduleHour, EditGradesScheduleSubjects, EditSeeRatingsStudents

urlpatterns = [    
    #editar
    path('grados/mirar/', SeeGrades.as_view(), name='MirarGrados'),

    #MIRAR ESTUDIANTES
    path('grados/mirar/estudiantes/<int:pk>/', SeeStudentsGrades.as_view(), name='VerEstudiantesGrado'),
    #MIRAR HORARIOS
    path('grados/mirar/horario/<int:pk>/', SeeGradesSchedules.as_view(), name='MirarGradoHorario'),
    #'APIS' PARA EL FORMULARIO DE HORARIOS
    path('grados/editar/horario/hora/<int:pk_post>/<int:pk_vista>/', EditGradesScheduleHour.as_view(), name='EditarHorarioHora'),
    path('grados/editar/horario/materias/<int:pk_post>/<int:pk_vista>/', EditGradesScheduleSubjects.as_view(), name='EditarHorarioMaterias'),
    #'APIS' PARA EDITAR VER NOTAS DE ALUMNOS #pk post = alumno
    path('grados/editar/ver/Notas/<int:pk_post>/<int:pk_vista>/', EditSeeRatingsStudents.as_view(), name='EditarVerNotasAlumnos'),
]