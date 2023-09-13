from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import RedirectUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('redirect/', RedirectUser.as_view(), name='RedirectUser'),
    #alumnos
    path('alumnos/', include('alumnos.urls')),
    path('acudientes/', include('acudientes.urls')),
    path('gestores/', include('gestores.urls')),
    path('administradores/', include('administradores.urls')),
    path('profesores/', include('profesores.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
