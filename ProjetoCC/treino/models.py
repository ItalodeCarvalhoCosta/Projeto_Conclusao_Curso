from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class SolicitacaoTreino(models.Model):
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    ]
    NIVEL_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    OBJETIVO_CHOICES = [
        ('hipertrofia', 'Hipertrofia'),
        ('emagrecimento', 'Emagrecimento'),
        ('forca', 'Força'),
        ('resistencia', 'Resistência'),
        ('saude_geral', 'Saúde geral'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="kg")
    altura = models.DecimalField(max_digits=4, decimal_places=2, help_text="metros, ex: 1.75")
    idade = models.PositiveIntegerField()
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    percentual_gordura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    nivel_experiencia = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='iniciante')
    objetivo_principal = models.CharField(max_length=20, choices=OBJETIVO_CHOICES)
    frequencia_semanal = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Dias por semana"
    )
    tempo_por_sessao = models.PositiveIntegerField(help_text="Minutos disponíveis por sessão")
    lesoes_dores = models.TextField(blank=True, help_text="Dores, limitações, lesões crônicas...")
    ficha_gerada = models.ForeignKey(
        'FichaTreino', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='solicitacao_origem'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitação de {self.usuario.username} em {self.criado_em.strftime('%d/%m/%Y')}"


class Exercicio(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class FichaTreino(models.Model):
    NIVEL_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fichas')
    nome = models.CharField(max_length=150, default='Minha ficha')
    objetivo = models.CharField(max_length=150, blank=True)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='iniciante')
    criado_em = models.DateTimeField(auto_now_add=True)
    exercicios = models.ManyToManyField(Exercicio, through='FichaExercicio', related_name='fichas')

    def __str__(self):
        return f"{self.nome} - {self.usuario}"


class FichaExercicio(models.Model):
    ficha = models.ForeignKey(FichaTreino, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=1)
    series = models.PositiveIntegerField(default=3)
    repeticoes = models.PositiveIntegerField(default=12)

    class Meta:
        ordering = ('ordem',)

    def __str__(self):
        return f"{self.exercicio.nome} na {self.ficha.nome} ({self.series}x{self.repeticoes})"