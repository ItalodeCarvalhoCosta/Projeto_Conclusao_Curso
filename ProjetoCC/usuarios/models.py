from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.

class Usuario(AbstractUser):

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

# Cliente

from django.db import models
from usuarios.models import Usuario


class Cliente(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE
    )

    data_nascimento = models.DateField()

    altura = models.FloatField()

    peso = models.FloatField()

    sexo = models.CharField(
        max_length=10,
        choices=[
            ('F', 'Feminino'),
            ('M', 'Masculino'),
        ]
    )

    objetivo = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.usuario.username