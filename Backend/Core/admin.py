from django.contrib import admin
from Autenticacao.models import USUARIO,SALARIO,COMISSAO
from Core.models import CLIENTE,ORDEN,CAIXA,SERVICO



admin.site.register(CAIXA)
admin.site.register(COMISSAO)
admin.site.register(CLIENTE)
admin.site.register(SERVICO)
admin.site.register(ORDEN)
admin.site.register(USUARIO)
admin.site.register(SALARIO)
