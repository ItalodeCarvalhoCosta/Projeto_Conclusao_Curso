from django import forms
from .models import Monitoramento


class MonitoramentoForm(forms.ModelForm):

    class Meta:
        model = Monitoramento

        fields = [
            'peso',
            'agua',
            'tempo_cardio',
            'seguiu_dieta',
            'realizou_treino',
        ]

        widgets = {
            'peso': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'Ex: 72.50'
                }
            ),

            'agua': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'Ex: 2.50'
                }
            ),

            'tempo_cardio': forms.NumberInput(
                attrs={
                    'min': '0',
                    'placeholder': 'Ex: 30'
                }
            ),
        }