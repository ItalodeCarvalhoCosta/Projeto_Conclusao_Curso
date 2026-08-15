from django import forms
from .models import FichaTreino, Exercicio


class FichaTreinoForm(forms.ModelForm):
    exercicios = forms.ModelMultipleChoiceField(
        queryset=Exercicio.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text='Escolha exercícios da biblioteca para incluir na ficha'
    )

    class Meta:
        model = FichaTreino
        fields = ('nome', 'objetivo', 'nivel', 'exercicios')
from django import forms
from .models import SolicitacaoTreino

class SolicitacaoTreinoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoTreino
        fields = ['problema_relatado']
        widgets = {
            'problema_relatado': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ex: tenho dor no joelho, prefiro treinar em casa...'
            }),
        }