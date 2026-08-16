from django.conf import settings
from django.db import models


class PlanoAlimentar(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planos_alimentares'
    )

    nome = models.CharField('nome do plano', max_length=150, default='Meu plano alimentar')

    calorias_meta = models.PositiveIntegerField('meta de calorias (kcal)', null=True, blank=True)
    proteina_meta = models.PositiveIntegerField('meta de proteína (g)', null=True, blank=True)
    carboidrato_meta = models.PositiveIntegerField('meta de carboidrato (g)', null=True, blank=True)
    gordura_meta = models.PositiveIntegerField('meta de gordura (g)', null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.nome} - {self.usuario.email}'


class Refeicao(models.Model):
    TIPO_CHOICES = [
        ('cafe', 'Café da manhã'),
        ('almoco', 'Almoço'),
        ('lanche', 'Lanche da tarde'),
        ('jantar', 'Jantar'),
    ]

    plano = models.ForeignKey(
        PlanoAlimentar,
        on_delete=models.CASCADE,
        related_name='refeicoes'
    )

    tipo = models.CharField('refeição', max_length=10, choices=TIPO_CHOICES)
    descricao = models.TextField('o que comer', help_text='Ex: Ovos mexidos, aveia, banana')

    calorias = models.PositiveIntegerField('calorias (kcal)', default=0)
    proteina = models.PositiveIntegerField('proteína (g)', default=0)
    carboidrato = models.PositiveIntegerField('carboidrato (g)', default=0)
    gordura = models.PositiveIntegerField('gordura (g)', default=0)

    class Meta:
        ordering = ['tipo']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.plano.nome}'
