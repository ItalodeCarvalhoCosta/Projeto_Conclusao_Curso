from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PerfilDieta(models.Model):
    """
    Armazena as informações que o usuário preenche para que a IA
    monte uma dieta personalizada: corpo, objetivo, alergias,
    restrições alimentares e orçamento disponível.
    """

    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    NIVEL_ATIVIDADE_CHOICES = [
        ('sedentario', 'Sedentário (pouco ou nenhum exercício)'),
        ('leve', 'Leve (exercício leve 1 a 3x/semana)'),
        ('moderado', 'Moderado (exercício moderado 3 a 5x/semana)'),
        ('intenso', 'Intenso (exercício pesado 6 a 7x/semana)'),
        ('muito_intenso', 'Muito intenso (exercício pesado + trabalho físico)'),
    ]

    OBJETIVO_CHOICES = [
        ('emagrecer', 'Emagrecer'),
        ('manter', 'Manter o peso'),
        ('ganhar_massa', 'Ganhar massa muscular'),
    ]

    RESTRICAO_CHOICES = [
        ('nenhuma', 'Nenhuma'),
        ('vegetariano', 'Vegetariano'),
        ('vegano', 'Vegano'),
        ('sem_gluten', 'Sem glúten'),
        ('sem_lactose', 'Sem lactose'),
        ('low_carb', 'Low carb'),
        ('outra', 'Outra (descrever abaixo)'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfis_dieta'
    )
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text='Peso em kg')
    altura = models.DecimalField(max_digits=4, decimal_places=2, help_text='Altura em metros. Ex: 1.75')
    idade = models.PositiveSmallIntegerField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    nivel_atividade = models.CharField(max_length=20, choices=NIVEL_ATIVIDADE_CHOICES)
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_CHOICES)

    restricao_alimentar = models.CharField(
        max_length=20, choices=RESTRICAO_CHOICES, default='nenhuma'
    )
    restricao_outra_descricao = models.CharField(
        max_length=200, blank=True,
        help_text='Preencha se escolheu "Outra" acima'
    )
    alergias = models.TextField(
        blank=True,
        help_text='Ex: amendoim, frutos do mar, lactose. Deixe em branco se não tiver.'
    )
    alimentos_que_nao_gosta = models.TextField(
        blank=True, help_text='Alimentos que prefere evitar, mesmo sem ser alergia'
    )
    condicoes_saude = models.TextField(
        blank=True, help_text='Ex: diabetes, hipertensão, colesterol alto'
    )

    orcamento_semanal = models.DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Quanto pode gastar com alimentação por semana, em R$'
    )
    refeicoes_por_dia = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(2), MaxValueValidator(8)],
        help_text='Quantas refeições prefere fazer por dia'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

def __str__(self):
    return f'Perfil de dieta de {self.usuario} - {self.criado_em:%d/%m/%Y}'


class DietaPersonalizada(models.Model):
    """
    Guarda a dieta que a IA gerou a partir de um PerfilDieta, junto
    com as metas de calorias e macros calculadas por calculos.py
    (essas metas são calculadas em Python, não pela IA, para garantir
    que os números batem com fórmulas nutricionais reconhecidas).
    """
    perfil = models.ForeignKey(
        PerfilDieta,
        on_delete=models.CASCADE,
        related_name='dietas_geradas'
    )

    calorias_alvo = models.PositiveIntegerField(help_text='Meta diária de calorias (kcal)')
    proteina_g = models.PositiveIntegerField(help_text='Meta diária de proteína (g)')
    carboidrato_g = models.PositiveIntegerField(help_text='Meta diária de carboidrato (g)')
    gordura_g = models.PositiveIntegerField(help_text='Meta diária de gordura (g)')

    conteudo_texto = models.TextField(help_text='Resposta bruta da IA, em texto')
    conteudo_json = models.JSONField(null=True, blank=True, help_text='Resposta estruturada, se disponível')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Dieta gerada para {self.perfil.usuario} em {self.criado_em:%d/%m/%Y}'