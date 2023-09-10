from django.urls import path
from .views import CreateAlumno, LoginAlumno
from . import views

urlpatterns = [
    path('crear/', CreateAlumno.as_view(), name='CrearAlumno'),
    path('login/', LoginAlumno.as_view(), name='LoginAlumno'),
]
