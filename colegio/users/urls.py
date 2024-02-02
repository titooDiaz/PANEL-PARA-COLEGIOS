from django.urls import path
from .views import GestionColegios
urlpatterns = [
    #### CREAR COLEGIO
    path('colegios/', GestionColegios.as_view(), name='Colegios'),
]