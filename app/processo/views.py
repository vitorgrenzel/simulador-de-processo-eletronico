from django.shortcuts import render
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, FormView

from django.urls import reverse_lazy
from processo.models import Processo
from processo.forms import InformacoesDoProcessoForm, DocumentosForm, ProcessoDocumentosForm
# from users.forms import UserCreateForm, UserCreatePassword, UserRecoverPassword, UserProfile, PasswordChangeForm

# PeticaoInicial
class InformacoesDoProcesso(CreateView):
    model = Processo
    form_class = InformacoesDoProcessoForm
    template_name = 'processo/peticao-inicial/informacoes.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('processo:peticao-inicial-assuntos', kwargs={'pk': self.object.id})


class Assuntos(UpdateView):
    model = Processo
    fields = [
        'competencia', 
        'assuntos',
        'assunto_principal',
    ]
    template_name = 'processo/peticao-inicial/assuntos.html'
   
    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('processo:peticao-inicial-parte-autora', kwargs={'pk': self.object.id})


class PartesAutoras(UpdateView):
    model = Processo
    fields = [
        'parte_autora', 
    ]
    template_name = 'processo/peticao-inicial/partes-autoras.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('processo:peticao-inicial-parte-reus', kwargs={'pk': self.object.id})

class PartesReus(UpdateView):
    model = Processo
    fields = [
        'parte_reus',
    ]
    template_name = 'processo/peticao-inicial/partes-reus.html'
    
    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('processo:peticao-inicial-documentos', kwargs={'pk': self.object.id})

class Documentos(UpdateView):
    model = Processo
    form_class = ProcessoDocumentosForm
    template_name = 'processo/peticao-inicial/documentos.html'
    success_url = reverse_lazy('processo:processo-relacao')


class ProcessoLista(ListView):
    """Add User view."""
    model = Processo
    template_name = 'processo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProcessoDetail(DetailView):
    model = Processo
    template_name = 'processo/detail.html'

    # def get_context_data(self, *args, **kwargs): 
    #     context = super(GeeksDetailView, 
    #          self).get_context_data(*args, **kwargs) 
    #     # add extra field  
    #     context["category"] = "MISC"        
    #     return context 

class ProcessoRelacao(ListView):
    """Add User view."""
    model = Processo
    template_name = 'processo/relacao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DocumentosCreate(CreateView):
    model = Documentos
    form_class = DocumentosForm
    template_name = 'processo/documentos-create.html'
    success_url = reverse_lazy('processo_lista')
