from django.urls import path
from .views import VerGrados

urlpatterns = [
    #editar
    path('grados/mirar/asdasd', VerGrados.as_view(), name='MirarGrados'),
]