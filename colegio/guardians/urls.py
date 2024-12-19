from django.urls import path
from .views import *

urlpatterns = [
    path('board/', AcudienteBoard.as_view(), name='BoardAcudiente'),
]