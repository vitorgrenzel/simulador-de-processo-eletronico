"""Processo urls."""
from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required

from processo.views import (
    ProcessoLista,
    InformacoesDoProcesso,
    Assuntos,
    PartesAutoras,
    PartesReus,
    Documentos,
    ProcessoDetail,
    ProcessoRelacao,
    DocumentosCreate
)

app_name = 'processo'
urlpatterns = [
    path(
        'listar/',
        login_required(ProcessoLista.as_view()),
        name='processo_lista'
    ),
    path('relacao/', login_required(ProcessoRelacao.as_view()), name='processo-relacao'),
    path('<slug:pk>', login_required(ProcessoDetail.as_view()), name='processo-detail'),
    path('peticao-inicial/', login_required(InformacoesDoProcesso.as_view()), name='peticao-inicial'),
    path('peticao-inicial/assuntos/<slug:pk>', login_required(Assuntos.as_view()), name='peticao-inicial-assuntos'),
    path('peticao-inicial/parte-autora/<slug:pk>', login_required(PartesAutoras.as_view()), name='peticao-inicial-parte-autora'),
    path('peticao-inicial/parte-reus/<slug:pk>', login_required(PartesReus.as_view()), name='peticao-inicial-parte-reus'),
    path('peticao-inicial/documentos/<slug:pk>', login_required(Documentos.as_view()), name='peticao-inicial-documentos'),
    path('documento/', login_required(DocumentosCreate.as_view()), name='processo-documento'),
]
