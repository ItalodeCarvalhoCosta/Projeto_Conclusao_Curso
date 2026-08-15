from django.conf import settings
from django.db import models
from django.utils import timezone


class Monitoramento(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='monitoramentos'
    )

    data = models.DateField(
        default=timezone.localdate
    )

    peso = models.DecimalField(
        'peso em kg',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    agua = models.DecimalField(
        'água consumida em litros',
        max_digits=4,
        decimal_places=2,
        default=0
    )

    tempo_cardio = models.PositiveIntegerField(
        'tempo de cardio em minutos',
        default=0
    )

    seguiu_dieta = models.BooleanField(
        'seguiu a dieta',
        default=False
    )

    realizou_treino = models.BooleanField(
        'realizou o treino',
        default=False
    )

    class Meta:
        ordering = ['-data']

        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'data'],
                name='monitoramento_unico_por_dia'
            )
        ]

    def calcular_imc(self):
        if self.peso and self.usuario.altura:
            altura = float(self.usuario.altura)

            if altura > 0:
                imc = float(self.peso) / (altura ** 2)
                return round(imc, 2)

        return None

    def __str__(self):
        return f'{self.usuario.nome} - {self.data}'