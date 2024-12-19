from django.urls import path
from .views import GestionColegios, Colegios, CreateGestorColegio, ViewColegios
urlpatterns = [
    #### CREAR COLEGIO
    path('colegios/crear/colegio/', GestionColegios.as_view(), name='ColegiosCreate'),
    
    ############################
    # Vista de administradores #
    ############################
    path('colegios/', Colegios.as_view(), name='Colegios'),
    # Crear colegios
    path('colegios/crear/gestor/', CreateGestorColegio.as_view(), name='ColegiosGestor'),
    # Mirar colegios
    path('colegios/view/', ViewColegios.as_view(), name='ViewColegiosADM')
]