from django.urls import path
from .views import VerGrados, VerGradosHorario

urlpatterns = [
    #editar
    path('grados/mirar/', VerGrados.as_view(), name='MirarGrados'),
    path('grados/mirar/horario/<int:pk>/', VerGradosHorario.as_view(), name='MirarGradoHorario'),
]