from django.contrib import admin
from Unidades.models import CUSTO,UNIDADE
from Autenticacao.models import USUARIO,SALARIO,COMISSAO
from Core.models import CLIENTE,ORDEN,SERVICO,SUB_SERVICO


admin.site.register(UNIDADE)
admin.site.register(CUSTO)
admin.site.register(COMISSAO)
admin.site.register(CLIENTE)
admin.site.register(ORDEN)
admin.site.register(SERVICO)
admin.site.register(SUB_SERVICO)
admin.site.register(USUARIO)
admin.site.register(SALARIO)
