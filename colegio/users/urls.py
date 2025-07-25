from django.urls import path
from .views import *

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
    path('colegios/view/', ViewColegios.as_view(), name='ViewColegiosADM'),
    path('colegios/profile/', ViewProfilePlus.as_view(), name='ViewProfilePlus'),
    # change password
    path('plus/profile/password/', ChangePassword.as_view(), name='ChangePasswordPlus'),
]