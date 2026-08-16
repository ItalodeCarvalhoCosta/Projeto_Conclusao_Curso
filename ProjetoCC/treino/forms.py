from django import forms
from .models import SolicitacaoTreino, FichaTreino, Exercicio


class SolicitacaoTreinoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoTreino
        fields = [
            'peso', 'altura', 'idade', 'genero', 'percentual_gordura',
            'nivel_experiencia', 'objetivo_principal', 'frequencia_semanal',
            'tempo_por_sessao', 'lesoes_dores',
        ]
        widgets = {
            'lesoes_dores': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ex: tenho dor no joelho, prefiro treinar em casa...'
            }),
        }


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