from django.urls import path
from .views import GestionColegios, Colegios, CreateGestorColegio
urlpatterns = [
    #### CREAR COLEGIO
    path('colegios/crear/colegio/', GestionColegios.as_view(), name='ColegiosCreate'),
    path('colegios/', Colegios.as_view(), name='Colegios'),
    path('colegios/crear/gestor/', CreateGestorColegio.as_view(), name='ColegiosGestor'),
]