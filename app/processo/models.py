"""Processo models."""
import uuid
import random

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from users.utils import generate_random_key

# from .managers import CustomUserManager

from users.models import User, Simulacao


class Assunto(models.Model):
    """Improved Assuntos model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(verbose_name=_('Assunto'), max_length=500, blank=False)
    class Meta:
        verbose_name = _('Assunto')
        verbose_name_plural = _('Assuntos')
    def __str__(self):
        return self.nome

class ClasseProcedural(models.Model):
    """Improved ClasseProcedural model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(verbose_name=_('Nome'), max_length=500, blank=False)
    class Meta:
        verbose_name = _('Classe Procedural')
        verbose_name_plural = _('Classes Procedurais')
    def __str__(self):
        return self.nome


class Documentos(models.Model):
    """Etapa Documento model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload = models.FileField(upload_to='uploads/documentos/')
    tipo = models.CharField(verbose_name=_('Tipo'), max_length=255, blank=False)
    sigilo = models.BooleanField(verbose_name=_('Sigilo'), default=False)

    class Meta:
        verbose_name = _('Documento')
        verbose_name_plural = _('Documentos')
    def __str__(self):
        return str(self.id)

class Processo(models.Model):
    """Improved Processo model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    simulacao = models.ForeignKey(Simulacao, on_delete=models.CASCADE)

    advogados = models.ManyToManyField(
        User,
        verbose_name=_('Advogados'),
        blank=True,
        related_name="user_advogado",
        related_query_name="user_advogado",
    )

    classe_procedural = models.ForeignKey(
        ClasseProcedural, 
        null=True,
        on_delete=models.CASCADE
    )
    localidade = models.CharField(
        verbose_name=_('Desejo entrar com ação em'),
        max_length=255, 
        null=True
    )
    rito = models.CharField(
        verbose_name=_('Rito'),
        max_length=500,
        null=True,
        choices=(
            ('RITO_ORDINÁRIO(COMUM)', _('RITO ORDINÁRIO (COMUM)')),
        )
    )
    area = models.CharField(
        verbose_name=_('ÁREA'),
        max_length=500,
        null=True,
        choices=(
            ('Cível - Ações Coletivas' , 'Cível - Ações Coletivas'),
            ('Cível - Cível' , 'Cível - Cível'),
            ('Cível - Empresas' , 'Cível - Empresas'),
            ('Cível - Recuperação Juridical e Falência' , 'Cível - Recuperação Juridical e Falência'),
            ('Cível - Registros Públicos' , 'Cível - Registros Públicos'),
            ('Familia/Sucessões/Curatelas' , 'Familia/Sucessões/Curatelas')
        )
    )
    nivel_sigilo = models.CharField(
        verbose_name=_('Sigilo'),
        max_length=500,
        null=True,
        choices=(
            ('0', 'Sem sigilo (Nível 0)'),
            ('1', 'Segredo de Justiça (Nível 1)'),
        )
    )
    valor_da_causa = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        null=True,
    )

    competencia = models.CharField(
        verbose_name=_('Competência'), 
        max_length=255, 
        blank=False, 
        null=True
    )

    assuntos = models.ManyToManyField(
        Assunto,
        verbose_name=_('Assuntos'),
        blank=True,
        related_name="assuntos_secundarios",
    )
    assunto_principal = models.ManyToManyField(
        Assunto,
        verbose_name=_('Assunto Principal'),
        blank=True,
        related_name="assuntos_principais",
    )

    parte_autora = models.ManyToManyField(
        User,
        verbose_name=_('Parte Autora'),
        blank=True,
        related_name="parte_autora",
    )
    parte_reus = models.ManyToManyField(
        User,
        verbose_name=_('Parte Réus'), 
        blank=True,
        related_name="parte_reus",
    )

    tramitação_doenca = models.BooleanField(verbose_name=_('Requer prioridade de tramitação - Doença grave'), default=False)
    tramitação_deficiencia = models.BooleanField(verbose_name=_('Requer prioridade de tramitação - Pessoa com deficiência'), default=False)
    antecipacao_tutela = models.BooleanField(verbose_name=_('Requer Liminar/Antecipação de Tutela'), default=False)
    tramitação_crianca = models.BooleanField(verbose_name=_('Requer prioridade de tramitação - Criança e Adolescente'), default=False)
    tramitação_idoso = models.BooleanField(verbose_name=_('Requer prioridade de tramitação - Idoso'), default=False)
    consiliacao = models.BooleanField(verbose_name=_('Manifesto que não tenho interesse em conciliar (art. 334, paragrafo 5°CPC)'), default=False)

    documentos = models.ManyToManyField(
        Documentos,
        verbose_name=_('Documentos'), 
        blank=True,
        related_name="processo_documentos",
    )

    class Meta:
        """User Meta settings."""
        verbose_name = _('Processo')
        verbose_name_plural = _('Processos')
        ordering = ['id']

    def __str__(self):
        """Return the model object string."""
        return 'Simulação: ' + self.simulacao.nome + ' - Identificador: ' + str(self.id)


class Evento(models.Model):
    """Evento model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(verbose_name=_('Descricao'), max_length=5000, blank=False)
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        """Evento Meta settings."""
        verbose_name = _('Evento')
        verbose_name_plural = _('Eventos')
        ordering = ['data']


class ParteAutora(models.Model):
    """ParteAutora model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(verbose_name=_('Descricao'), max_length=5000, blank=False)
    cpf = models.CharField(verbose_name=_('CPF'), max_length=5000, blank=False)
    cnpj = models.CharField(verbose_name=_('CNPJ'), max_length=5000, blank=False)

    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, null=True)

    class Meta:
        """Evento Meta settings."""
        verbose_name = _('Parte Autora')
        verbose_name_plural = _('Partes Autoras')
        ordering = ['nome']

class Etapa(models.Model):
    """Evento model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(verbose_name=_('Nome'), max_length=255, blank=False)
    preocesso = models.ManyToManyField(
        Processo,
        verbose_name=_('Processo Etapa'),
        blank=False,
        related_name="etapa_processo",
        related_query_name="etapa_processo",
    )

    class Meta:
        """Evento Meta settings."""
        verbose_name = _('Etapa')
        verbose_name_plural = _('Etapas')
        
class EtapaDocumento(models.Model):
    """Etapa Documento model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload = models.FileField(upload_to='uploads/documentos/')
    #tipo = models.CharField(verbose_name=_('Nome'), max_length=255, blank=False)
    sigilo = models.BooleanField(verbose_name=_('Nome'), default=False)
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Etapa Documento')
        verbose_name_plural = _('Etapas Documentos')
