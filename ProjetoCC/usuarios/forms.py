from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'nome')

class PerfilForm(forms.ModelForm):
            class Meta:
                model = Usuario
                fields = ('nome', 'altura', 'email', 'sexo' )