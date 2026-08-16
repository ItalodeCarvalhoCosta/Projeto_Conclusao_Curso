from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nome, password, **extra_fields)


class Usuario(AbstractUser):
    username = None  # removemos o username padrão
    email = models.EmailField('email', unique=True)
    nome = models.CharField('nome completo', max_length=150)
    altura = models.DecimalField(
        'altura em metros',
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )
    

    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino'), ]
    sexo = models.CharField(
        'sexo',
        max_length=1,
        choices=SEXO_CHOICES,
        null=True,
        blank=True
    )

    data_nascimento = models.DateField(
        'data de nascimento',
        null=True,
        blank=True
    )

    NIVEL_ATIVIDADE_CHOICES = [
        ('sedentario', 'Sedentário (pouco ou nenhum exercício)'),
        ('leve', 'Levemente ativo (exercício leve, 1 a 3x por semana)'),
        ('moderado', 'Moderadamente ativo (exercício moderado, 3 a 5x por semana)'),
        ('intenso', 'Altamente ativo (exercício intenso, 6 a 7x por semana)'),
        ('muito_intenso', 'Extremamente ativo (exercício muito intenso ou trabalho físico)'),
    ]
    nivel_atividade = models.CharField(
        'nível de atividade física',
        max_length=20,
        choices=NIVEL_ATIVIDADE_CHOICES,
        null=True,
        blank=True
    )

    OBJETIVO_CHOICES = [
        ('emagrecimento', 'Emagrecimento'),
        ('hipertrofia', 'Hipertrofia (ganho de massa muscular)'),
        ('manutencao', 'Manutenção do peso'),
    ]
    objetivo = models.CharField(
        'objetivo',
        max_length=20,
        choices=OBJETIVO_CHOICES,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'   # login será feito com email
    REQUIRED_FIELDS = ['nome']  # pedido ao criar superuser

    objects = UsuarioManager()
    @property
    def idade(self):
        if not self.data_nascimento:
            return None

        from datetime import date
        hoje = date.today()

        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    def __str__(self):
        return self.email