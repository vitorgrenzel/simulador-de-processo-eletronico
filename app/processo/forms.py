# """Products forms."""
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from searchableselect.widgets import SearchableSelect
from django.utils.translation import gettext_lazy as _
from django.forms import ClearableFileInput

from processo.models import Processo, Documentos
from users.models import User, Turma, Simulacao 


class InformacoesDoProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        exclude = ()
        # widgets = {
        #     'advogados': SearchableSelect(
        #         model='processo.advogados', 
        #         search_field='nome',
        #         many=True,
        #         limit=10000
        #     )
        # }
        fields = [
            'localidade', 
            'rito',
            'area',
            'nivel_sigilo',
            'classe_procedural',
            'valor_da_causa',
            'advogados',
            'simulacao'
        ]

    def __init__(self, *args, **kwargs):
        print("\n ----------  __init__  ------------- \n")
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     print("\n ----------  SAVE  ------------- \n")
    #     instance = super().save(commit=True)
    #     print(self.user)
    #     turma = Turma.objects.filter(User=self.user)
    #     print("Turma: ", turma)
    #     simulacao = Simulacao.objects.filter(turma=turma)
    #     print("Simulacao: ", simulacao)
    #     instance.simulacao_id = simulacao.get('id')
    #     instance.save()
    #     instance.save()


class ProcessoDocumentosForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = [
            'tramitação_doenca',
            'tramitação_deficiencia',
            'antecipacao_tutela',
            'tramitação_crianca',
            'tramitação_idoso',
            'consiliacao',
            'documentos'
        ]


class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = [
            'tipo',
            'sigilo',
            'upload',
        ]
        

    # def save(self, commit=True):
    #     instance = super().save(commit=True)
    #     turma = Turma.objects.filter(User=self.user)
    #     # Adiciona petição inicial a etapa
    #     # Vincula documentos ao processo e a etapa
    #     instance.save()
    #     instance.save()

# class ParteAutoraForm(forms.ModelForm):
#     groups = ModelMultipleChoiceField(
#         label=_('Profile List'),
#         queryset=Profile.objects.all().annotate(num_perm=Count('permissions')).filter(num_perm=0), 
#         required=True,
#         widget=FilteredSelectMultiple(
#             verbose_name=Profile._meta.verbose_name,
#             is_stacked=False
#         )
#     )


