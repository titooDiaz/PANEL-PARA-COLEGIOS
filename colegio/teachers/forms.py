from django import forms
from information.models import Activities, File, Rating
from django.forms.widgets import *
from users.models import *


#TRANSLATE: FilesProfesoresForm
class FilesProfesoresForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off','id':'nombre','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo de la actividad'}),
            
            'description': forms.TextInput(attrs={'autocomplete': 'off','id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripccion del documento de la actividad'}),
            
            'file': forms.FileInput(attrs={'id':'archivo', 'class': 'hidden'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


#TRANSLATE: ActividadesForm
class ActivitiesForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    class Meta:
        model = Activities
        fields = ['name', 'description', 'type', 'percentage', 'start_date', 'end_date', 'start_time', 'end_time', 'time_zone', 'location_time_zone']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off','id':'titulo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:border-red-600 block w-full p-2.5', 'placeholder': 'Titulo de la actividad'}),
            
            'location_time_zone': forms.TextInput(attrs={'autocomplete': 'off','id':'location_time_zone','class': 'hidden'}),

            'description': forms.TextInput(attrs={'autocomplete': 'off','id':'descripcion','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:border-red-600 block w-full p-2.5', 'placeholder': 'Descripcion de la actividad'}),
            
            'percentage': forms.NumberInput(attrs={'autocomplete': 'off','id':'porcentaje','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:border-red-600 block w-full p-2.5', 'placeholder': 'porcentaje de la actividad', 'min': 1, 'max': 100}),

            'type': forms.Select(attrs={'id':'tipo','class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:border-red-600 block w-full p-2.5'}),
            
            'start_time': forms.TimeInput(attrs={'id':'hora_inicio','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            
            'start_date': forms.DateInput(attrs={'id':'fecha_inicio','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),
            
            'end_time': forms.TimeInput(attrs={'id':'hora_final','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'time'}),
            
            'end_date': forms.DateInput(attrs={'id':'fecha_final','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300', 'type':'date'}),

            'time_zone': forms.CheckboxInput(attrs={'id':'zona_horaria','class': 'mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-orange-300 focus:ring-orange-600 w-full h-12',}),

        }


class FileForm(forms.Form):
    archivo = forms.FileField(widget=forms.ClearableFileInput())
    
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'message']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'hidden','id':'rating'}),
            
            'message': forms.TextInput(attrs={'autocomplete': 'off','id':'message','class': 'border border-gray-800 text-gray-900 text-sm rounded-lg focus:border-red-600 block m-2 p-1', 'placeholder': 'Mensaje al estudiente'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomUserTeacherEditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUserTeachers
        fields = ('first_name', 'last_name', 'email')
        widgets = {  
            'first_name': forms.TextInput(attrs={
                'autocomplete': 'off',
                'id': 'first_name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Nombres del usuario'
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'last_name',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Apellidos del usuario'
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'off',
                'id': 'email',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-red-600 focus:border-red-600 block w-full p-2.5',
                'placeholder': 'Email donde se puede contactar al usuario'
            }),
        }               
