"""users models"""
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

# from django.urls import reverse
# from django.utils.translation import gettext_lazy as _

# from core import defaults
# from core.fields import StaticImageField
# from metadata.models import (AcademicDegree, AddressType, DocumentType, Gender,
#                              Institution, LinkType, Nationality, Race,
#                              ResearchArea)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User model."""

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True, verbose_name='E-mail de login')
    nickname = models.CharField(max_length=256, verbose_name='Apelido')
    full_name = models.CharField(max_length=256, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, null=True, blank=True, verbose_name='CPF')
    # username = models.CharField(max_length=1, null=True, blank=True)

    # picture = StaticImageField(
    #     blank=True,
    #     null=True,
    #     default_image_path='img/default.jpg',
    #     verbose_name='Foto do perfil'
    # )
    code = models.CharField(max_length=7, unique=True, blank=True, null=True, verbose_name='Matrícula')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['full_name']

    def __str__(self):
        return self.email


# class Document(models.Model):
#     ''' User documents '''
#     user = models.ForeignKey(User, models.CASCADE, related_name='documents')
#     doc_type = models.ForeignKey(
#         DocumentType,
#         models.CASCADE,
#         related_name='documents',
#         verbose_name=_('Tipo de documento')
#     )
#     number = models.CharField(max_length=256, verbose_name=_('Número'))

#     class Meta:
#         ordering = ['number']
#         verbose_name = _('Documento')
#         verbose_name_plural = _('Documentos')
#         default_permissions = ()

#     def __str__(self):
#         return self.number
