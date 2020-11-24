"""Users models."""
import uuid
import random
import datetime

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from users.utils import generate_random_key

from .managers import CustomUserManager


class Papel(Group):
    """Papel model."""
    class Meta:
        proxy = True
        verbose_name = _('Papel')
        verbose_name_plural = _('Papeis')
        app_label = 'users'
# simulacao = models.ForeignKey(Simulacao, on_delete=models.CASCADE)
# usuario = models.ForeignKey(User, on_delete=models.CASCADE)
# name = models.CharField(
#     verbose_name=_('Papel'),
#     max_length=255,
#     choices=(
#         ('ADVOGADO_AUTOR', _('Advogado autor')),
#         ('ADVOGADO_REU', _('Advogado réu')),
#         ('JUIZ', _('Juiz')),
#         ('MP', _('Ministério público')),
#     )
# )

class User(AbstractUser):
    """Improved User model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(verbose_name=_('E-mail'), blank=False, unique=True)
    nome = models.CharField(verbose_name=_('Nome'), max_length=255, blank=False, null=True)
    matricula = models.CharField(verbose_name=_('Matricula'), max_length=7, blank=False)
    alterar_senha = models.CharField(verbose_name=_('Alterar Senha'), max_length=33, blank=True, default=generate_random_key)
    groups = models.ManyToManyField(
        Papel,
        verbose_name=_('Papeis'),
        blank=False,
        help_text=_(
            'The profile this user belongs to. A user will get all permissions '
            'granted to each of their profiles.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    class Meta:
        """User Meta settings."""
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        # ordering = ['first_name', 'last_name', 'username']

    # def __str__(self):
    #     """Return the model object string."""
    #     return self.get_full_name() or self.get_username()


class Turma(models.Model):
    """Turma model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(verbose_name=_('Nome'), max_length=255, blank=False)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    usuarios = models.ManyToManyField(
        User, 
        verbose_name=_('Usuários'),
        blank=False,
        related_name="usuario_turma",
        related_query_name="user",
    )

    class Meta:
        """Turma Meta settings."""
        verbose_name = _('Turma')
        verbose_name_plural = _('Turmas')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Simulacao(models.Model):
    """Simulacao model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(verbose_name=_('Nome'), max_length=255, blank=False)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True)

    class Meta:
        """Simulacao Meta settings."""
        verbose_name = _('Simulação')
        verbose_name_plural = _('Simulações')
        ordering = ['nome']

    def __str__(self):
        return self.nome 