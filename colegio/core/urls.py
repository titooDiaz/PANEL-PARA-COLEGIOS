from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import RedirectUser
from django.shortcuts import redirect

urlpatterns = [
    #ADMINISTRADOR DE APP
    path('admin/', admin.site.urls),  # Asegúrate de tener esta línea también

    
    #HOME
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    #contact us
    path('contact/', TemplateView.as_view(template_name='home_menu/contact.html'), name='contact'),
    
    #about 
    path('about/', TemplateView.as_view(template_name='home_menu/about.html'), name='about'),
    
    #USUARIOS
    path('accounts/', include('allauth.urls')),
    path('redirect/', RedirectUser.as_view(), name='RedirectUser'),
    
    #URLS DE PERSONAS
    path('alumnos/', include('students.urls')),
    path('users/', include('users.urls')),
    path('acudientes/', include('guardians.urls')),
    path('gestores/', include('managers.urls')),
    path('informacion/', include('information.urls')),
    path('administradores/', include('admins.urls')),
    path('profesores/', include('teachers.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
