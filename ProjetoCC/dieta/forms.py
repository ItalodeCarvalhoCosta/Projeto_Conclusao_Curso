from django import forms
from .models import PerfilDieta


class PerfilDietaForm(forms.ModelForm):
    class Meta:
        model = PerfilDieta
        exclude = ['usuario', 'criado_em', 'atualizado_em']
        widgets = {
            'alergias': forms.Textarea(attrs={'rows': 2}),
            'alimentos_que_nao_gosta': forms.Textarea(attrs={'rows': 2}),
            'condicoes_saude': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned = super().clean()
        restricao = cleaned.get('restricao_alimentar')
        descricao = cleaned.get('restricao_outra_descricao')
        if restricao == 'outra' and not descricao:
            self.add_error(
                'restricao_outra_descricao',
                'Descreva a restrição alimentar.'
            )
        return cleaned