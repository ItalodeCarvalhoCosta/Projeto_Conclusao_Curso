from django import forms
from .models import PerfilTreino


class PerfilTreinoForm(forms.ModelForm):
    """
    Formulário que o usuário preenche com peso, altura, idade, objetivo,
    etc. O campo `usuario` é setado na view (request.user), não aqui.
    """

    class Meta:
        model = PerfilTreino
        exclude = ['usuario', 'criado_em', 'atualizado_em']
        widgets = {
            'problemas_saude': forms.Textarea(attrs={'rows': 3}),
            'lesoes_dores': forms.Textarea(attrs={'rows': 3}),
        }