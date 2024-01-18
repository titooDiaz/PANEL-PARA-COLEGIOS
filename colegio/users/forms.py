from django import forms
from allauth.account.forms import PasswordField
from allauth.account.forms import SignupForm, LoginForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(LoginForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'password'}),
    )