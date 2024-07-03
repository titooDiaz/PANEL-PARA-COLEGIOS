from django.urls import path
from .views import *

urlpatterns = [
    path('board/', BoardProfesores.as_view(), name='BoardProfesores'),
    path('view/actividades/<int:pk>', ViewActividades.as_view(), name='ViewActividades'),
]