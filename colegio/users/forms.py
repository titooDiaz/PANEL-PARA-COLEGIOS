from django import forms
from allauth.account.forms import SignupForm, LoginForm
from .models import Colegio

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(LoginForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'password'}),
    )
    
class ColegioForm(forms.ModelForm):
    class Meta:
        model = Colegio
        fields = ['colegio_nom', 'numero', 'direccion', 'descripcion', 'foto', 'banner']
        widgets = {}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)