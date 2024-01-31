from django.urls import path
from .views import *

urlpatterns = [
    path('board/', BoardProfesores.as_view(), name='BoardProfesores'),
]