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

    