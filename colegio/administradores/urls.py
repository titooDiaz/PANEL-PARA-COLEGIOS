from django.urls import path
from .views import *

urlpatterns = [
    path('board/', AdministradorBoard.as_view(), name='BoardAlumno'),
]