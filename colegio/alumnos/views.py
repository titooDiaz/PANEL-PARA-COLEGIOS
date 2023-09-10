from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import CustomUserAlumnoForm, CustomAlumnoLoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend


class CreateAlumno(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
        return render(request, 'users/alumnos/create_alumnos.html', context)
    def get(self, request, *args, **kwargs):
        form = CustomUserAlumnoForm()
        context = {
            'form': form
        }
        return render(request, 'users/alumnos/create_alumnos.html', context)



class LoginAlumno(View):
    def post(self, request, *args, **kwargs):
        form = CustomAlumnoLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Cambia 'home' por la URL a la que quieres redirigir después de iniciar sesión
        return render(request, 'users/alumnos/login.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = CustomAlumnoLoginForm()
        return render(request, 'users/alumnos/login.html', {'form': form})
