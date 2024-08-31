from django.shortcuts import render, get_object_or_404, redirect
from .models import Colegio
from django.views.generic import TemplateView, View
from .forms import ColegioForm
from PIL import Image
import io
from django.contrib import messages
from django.core.files.base import ContentFile

## MENSAJES DE ERRORES ##
from message_error import messages_error

from .forms import CustomUserGestorForm

def recorte_imagenes(cords, foto):
    cords = cords.split(',')
    coordenadas_recorte = (
        int(cords[0]),
        int(cords[1]),
        int(cords[0]) + int(cords[2]),
        int(cords[1]) + int(cords[3])
    )

    imagen_original = Image.open(foto)
    imagen_recortada = imagen_original.crop(coordenadas_recorte)

    # Crear un objeto de archivo en memoria y guardar la imagen recortada en él
    image_io = io.BytesIO()
    imagen_recortada.save(image_io, format='PNG')#GUARDAMOS LA NUEVA IMAGEN EN FORMATO PNG EN LA VARIABLE 'image_io'
    return image_io

class Colegios(View):
    def get(self, request):
        colegios = Colegio.objects.all()
        form = ColegioForm()
        vista = 'plus'
        abierto='colegio'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
            'colegios': colegios
        }
        return render(request, 'colegios/Opciones.html', context)

class GestionColegios(View):
    def get(self, request):
        colegios = Colegio.objects.all()
        form = ColegioForm()
        vista = 'plus'
        abierto='colegio'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
            'colegios': colegios
        }
        return render(request, 'colegios/CreateColegio.html', context)

    def post(self, request):
        form = ColegioForm(request.POST, request.FILES)
        # Acceder a la foto del formulario
        if form.is_valid():
            foto = form.cleaned_data.get('foto')
            banner = form.cleaned_data.get('banner')

            if foto != 'colegiosFoto/profile.png' :
                cords = form['cords'].value()
                cords= cords.split(':')
                cords = cords[0]
                
                image_io = recorte_imagenes(cords, foto)
                # Asignar el objeto de archivo al campo 'foto'
                form.instance.foto.save('profile.png', ContentFile(image_io.getvalue()))
                
            if banner != 'colegiosBanner/banner.png':
                cords = form['cords'].value()
                cords= cords.split(':')
                cords = cords[1]
                
                image_io = recorte_imagenes(cords, banner)
                # Asignar el objeto de archivo al campo 'foto'
                form.instance.banner.save('banner.png', ContentFile(image_io.getvalue()))
                

            # Guardar el formulario para actualizar la instancia del modelo
            form.save()
            messages.success(request, 'Colegio agregado correctamente!')
        else:
            mensaje = "¡Hubo un error al agregar el Colegio!"
            messages_error.errores_formularios(form.errors, mensaje, request)
        return redirect('ColegiosCreate')
    
    
class CreateGestorColegio(View):
    def post(self, request, *args, **kwargs):
        form = CustomUserGestorForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            gestor = form.save(commit=False)
            gestor.numero_documento = username
            gestor.save()
            messages.success(request, '¡Gestor agregado correctamente!')
        else:
            print(form.errors)
            mensaje = "¡Hubo un error al agregar el gestor!"
            messages_error.errores_formularios(form.errors, mensaje, request)
        return redirect('ColegiosGestor')
    def get(self, request, *args, **kwargs):
        form = CustomUserGestorForm()
        vista = 'plus'
        abierto='colegio'
        context = {
            'form': form,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'colegios/AgregarGestor.html', context)
    
class ViewColegios(View):
    def get(self, request, *args, **kwargs):
        colegios = Colegio.objects.all()
        vista = 'plus'
        abierto='colegio'
        context = {
            'colegios': colegios,
            'vista': vista,
            'abierto':abierto,
        }
        return render(request, 'colegios/VerColegios.html', context)