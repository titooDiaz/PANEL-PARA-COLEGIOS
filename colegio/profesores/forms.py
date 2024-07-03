from django import forms
from informacion.models import Actividades, Archivo

class ActividadesForm(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['ano_creacion', 'titulo', 'descripcion', 'estado', 'author', 'horario_partes', 'grado']


class ArchivoForm(forms.Form):
    archivo = forms.FileField(widget=forms.ClearableFileInput())
