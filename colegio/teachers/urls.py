from django.urls import path
from .views import *

urlpatterns = [
    path('board/', BoardTeachers.as_view(), name='BoardTeachers'),
    path('actividades/create/<int:pk>', CreateActividades.as_view(), name='CreateActividades'),
    path('actividades/view/<int:pk>', ViewActividades.as_view(), name='ViewActividades'),
    path('actividades/rating/<int:student_pk>/<int:activity_pk>', RatingStudentActivity.as_view(), name='RatingStudentActivities'),
    path('edit/actividades/<int:pk>', EditActividades.as_view(), name='EditActividades'),
    
    # es - Ver horario
    # en - View schedule
    path('view/schedule/', ProfessorSchedule.as_view(), name='ViewScheduleProfessor'),
    
    # es - Ver Mensajes
    # en - View Messages
    path('view/messages/', ProfessorMessages.as_view(), name='ViewScheduleMessages'),
    
    # es - Ver Personas
    # en - View People
    path('view/people/', ProfessorPeople.as_view(), name='ViewSchedulePeople'),
    
    # es - Mensajes
    # en - Messages
    path('mensajes/', ProfessorMessages.as_view(), name='MessagesTeachers'),
    
    # es - Ver Notas
    # en - View Ratings
    path('view/ratings/', ProfessorRatings.as_view(), name='ViewScheduleRatings'),

    #profile
    path('teacher/profile/', ViewProfile.as_view(), name='ViewProfileTeacher'),
    # change password
    path('teacher/profile/password/', ChangePassword.as_view(), name='ChangePasswordTeacher'),
]