from django.urls import path
from .views import *

urlpatterns = [
    path('board/', BoardProfesores.as_view(), name='BoardProfesores'),
    path('actividades/create/<int:pk>', CreateActividades.as_view(), name='CreateActividades'),
    path('edit/actividades/<int:pk>', EditActividades.as_view(), name='EditActividades'),
]