from django.urls import path
from .views import CreateGestor, ViewUsersSettings, BoardGestores, CalendarioGestores, MensajesGestores, AjustesGestores, CreateAlumno

urlpatterns = [
    #ver usuarios para modificar o ...
    path('board/', BoardGestores.as_view(), name='BoardGestores'),
    path('calendario/', CalendarioGestores.as_view(), name='CalendarioGestores'),
    path('mensajes/', MensajesGestores.as_view(), name='MensajesGestores'),
    path('personas/', ViewUsersSettings.as_view(), name='ViewUsersSettings'),
    path('ajustes/', AjustesGestores.as_view(), name='AjustesGestores'),

    path('crear/gestores/', CreateGestor.as_view(), name='CrearGestor'),
    path('crear/alumnos', CreateAlumno.as_view(), name='CrearAlumno'),
]