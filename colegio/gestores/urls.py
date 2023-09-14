from django.urls import path
from .views import CreateGestor, ViewUsersSettings

urlpatterns = [
    #ver usuarios para modificar o ...
    path('personas/', ViewUsersSettings.as_view(), name='ViewUsersSettings'),

    path('crear/', CreateGestor.as_view(), name='CrearGestor'),
]