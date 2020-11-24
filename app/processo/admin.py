from django.contrib import admin

from processo.models import Processo, Evento, Assunto, Documentos, ParteAutora, Etapa, EtapaDocumento, ClasseProcedural

# Register your models here.
admin.site.register(Processo)
admin.site.register(Evento)
admin.site.register(Assunto)
admin.site.register(Documentos)
admin.site.register(ParteAutora)
admin.site.register(Etapa)
admin.site.register(EtapaDocumento)
admin.site.register(ClasseProcedural)
