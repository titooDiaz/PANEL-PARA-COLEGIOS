from django import forms
from informacion.models import Actividades_Respuesta_Estudiantes

class ActividadesRespuestaForm(forms.ModelForm):
    class Meta:
        model = Actividades_Respuesta_Estudiantes
        fields = ['respuesta', 'descripcion', 'fecha_entrega', 'hora_entrega', 'lugar_zona_horaria', 'misma_zona']

