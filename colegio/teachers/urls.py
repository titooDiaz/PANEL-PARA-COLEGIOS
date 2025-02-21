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
]