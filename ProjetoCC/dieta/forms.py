from django import forms
from .models import PlanoAlimentar, Refeicao


class PlanoAlimentarForm(forms.ModelForm):
    class Meta:
        model = PlanoAlimentar
        fields = ('nome', 'calorias_meta', 'proteina_meta', 'carboidrato_meta', 'gordura_meta')


class RefeicaoForm(forms.ModelForm):
    class Meta:
        model = Refeicao
        fields = ('tipo', 'descricao', 'calorias', 'proteina', 'carboidrato', 'gordura')
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }