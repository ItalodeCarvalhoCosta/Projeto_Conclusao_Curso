from django.db import models
from django.conf import settings
# Use settings.AUTH_USER_MODEL to support custom user models

class Treino(models.Model):
    NIVEL_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    grupo_muscular = models.CharField(max_length=100, blank=True)  # ex: "Peito", "Costas"
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='iniciante')
    series = models.PositiveIntegerField(default=3)
    repeticoes = models.PositiveIntegerField(default=12)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class SolicitacaoTreino(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problema_relatado = models.TextField(blank=True, help_text="Dores, limitações, preferências...")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitação de {self.usuario.username} em {self.criado_em.strftime('%d/%m/%Y')}"

    

class Exercicio(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True, help_text="Link para vídeo demonstrativo (YouTube, Vimeo etc)")
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
        return f"{self.nome} - {self.usuario.email}"


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

