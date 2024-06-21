from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from users.models import CustomUser, CustomUserAdministrador, CustomUserAlumno

class RedirectUser(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'customuseralumno'):
                return redirect('BoardAlumno')
            elif hasattr(request.user, 'customuserprofesores'):
                return redirect('BoardProfesores')
            elif hasattr(request.user, 'customuseradministrador'):
                return redirect('BoardAdministrador')
            elif hasattr(request.user, 'customusergestor'):
                return redirect('BoardGestores')
            elif hasattr(request.user, 'customuseracudiente'):
                return redirect('BoardAcudiente')
            else:
                return redirect('Colegios')
        else:
            return redirect('home')