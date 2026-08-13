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