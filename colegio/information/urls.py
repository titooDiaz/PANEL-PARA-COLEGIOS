from django.urls import path
from .views import SeeGrades, SeeGradesSchedules, SeeStudentsGrades, SendMessageView

#'APIS'
from .views import EditGradesScheduleHour, EditGradesScheduleSubjects, EditSeeRatingsStudents, upload_chat_file

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

    # messages
    path('send/', SendMessageView.as_view(), name='send-message'),
    
    # File By AJAX
    path('upload-chat-file/', upload_chat_file, name='upload_chat_file'),
]