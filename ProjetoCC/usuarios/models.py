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

    USERNAME_FIELD = 'email'   # login será feito com email
    REQUIRED_FIELDS = ['nome']  # pedido ao criar superuser

    objects = UsuarioManager()

    def __str__(self):
        return self.email