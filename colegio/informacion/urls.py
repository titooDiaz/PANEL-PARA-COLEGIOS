from django.urls import path
from .views import VerGrados, VerGradosHorario

#'APIS' de formualrio de horarios
from .views import EditarGradosHorarioHora, EditarGradosHorarioJueves, EditarGradosHorarioLunes, EditarGradosHorarioMartes, EditarGradosHorarioMiercoles, EditarGradosHorarioViernes

urlpatterns = [
    #editar
    path('grados/mirar/', VerGrados.as_view(), name='MirarGrados'),
    path('grados/mirar/horario/<int:pk>/', VerGradosHorario.as_view(), name='MirarGradoHorario'),

    #'APIS' PARA EL FORMULARIO DE HORARIOS
    path('grados/editar/horario/lunes/<int:pk>/', EditarGradosHorarioLunes.as_view(), name='EditarHorarioLunes'),
    path('grados/editar/horario/martes/<int:pk>/', EditarGradosHorarioMartes.as_view(), name='EditarHorarioMartes'),
    path('grados/editar/horario/Miercoles/<int:pk>/', EditarGradosHorarioMiercoles.as_view(), name='EditarHorarioMiercoles'),
    path('grados/editar/horario/jueves/<int:pk>/', EditarGradosHorarioJueves.as_view(), name='EditarHorarioJueves'),
    path('grados/editar/horario/viernes/<int:pk>/', EditarGradosHorarioViernes.as_view(), name='EditarHorarioViernes'),
    path('grados/editar/horario/hora/<int:pk>/', EditarGradosHorarioHora.as_view(), name='EditarHorarioHora'),
]