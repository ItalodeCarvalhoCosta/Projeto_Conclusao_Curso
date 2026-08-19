from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PerfilTreino(models.Model):
    """
    Armazena as informações que o usuário preenche (peso, altura, objetivo,
    etc.) para que a IA monte um treino personalizado.
    """

    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    NIVEL_EXPERIENCIA_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]

    OBJETIVO_CHOICES = [
        ('emagrecer', 'Emagrecer'),
        ('ganhar_massa', 'Ganhar massa muscular'),
        ('manter', 'Manter o condicionamento'),
        ('definicao', 'Definição muscular'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfis_treino'
    )
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text='Peso em kg')
    altura = models.DecimalField(max_digits=4, decimal_places=2, help_text='Altura em metros. Ex: 1.75')
    idade = models.PositiveSmallIntegerField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    percentual_gordura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        help_text='Percentual de gordura corporal, se souber'
    )
    nivel_experiencia = models.CharField(max_length=20, choices=NIVEL_EXPERIENCIA_CHOICES)
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_CHOICES)
    problemas_saude = models.TextField(blank=True, help_text='Problemas de saúde relevantes')
    frequencia_semanal = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text='Quantos dias por semana pretende treinar'
    )
    tempo_por_sessao = models.PositiveSmallIntegerField(help_text='Tempo disponível por treino, em minutos')
    lesoes_dores = models.TextField(blank=True, help_text='Lesões ou dores atuais')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Perfil de {self.usuario} - {self.criado_em:%d/%m/%Y}'


class TreinoPersonalizado(models.Model):
    """
    Guarda o treino que a IA gerou a partir de um PerfilTreino.
    """
    perfil = models.ForeignKey(
        PerfilTreino,
        on_delete=models.CASCADE,
        related_name='treinos_gerados'
    )
    conteudo_texto = models.TextField(help_text='Resposta bruta da IA, em texto')
    conteudo_json = models.JSONField(null=True, blank=True, help_text='Resposta estruturada (dias/exercícios), se disponível')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Treino gerado para {self.perfil.usuario} em {self.criado_em:%d/%m/%Y}'


class Exercicio(models.Model):
    """
    Biblioteca de exercícios (nome, imagem, link do YouTube).
    Só o administrador cria/edita/apaga, pelo Django Admin.
    O usuário comum só pode visualizar.
    """

    GRUPO_MUSCULAR_CHOICES = [
        ('peito', 'Peito'),
        ('costas', 'Costas'),
        ('pernas', 'Pernas'),
        ('ombro', 'Ombro'),
        ('biceps', 'Bíceps'),
        ('triceps', 'Tríceps'),
        ('abdomen', 'Abdômen'),
        ('gluteos', 'Glúteos'),
        ('cardio', 'Cardio'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=100)

    grupo_muscular = models.CharField(
        max_length=20,
        choices=GRUPO_MUSCULAR_CHOICES,
        default='outro'
    )

    imagem = models.ImageField(
        upload_to='exercicios/',
        blank=True,
        null=True
    )

    link_youtube = models.URLField(
        help_text='Link do vídeo de referência no YouTube'
    )

    descricao = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome