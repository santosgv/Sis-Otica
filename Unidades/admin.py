from django.contrib import admin
from Unidades.models import CLIENTE, CLIENTE_EXAME, COMISSAO, CUSTO, LONGE, ORDEM_SERVICO, PERTO, SALARIO, UNIDADE
from Autenticacao.models import Usuario


admin.site.register(UNIDADE)
admin.site.register(CUSTO)
admin.site.register(SALARIO)
admin.site.register(COMISSAO)
admin.site.register(LONGE)
admin.site.register(PERTO)
admin.site.register(CLIENTE)
admin.site.register(CLIENTE_EXAME)
admin.site.register(ORDEM_SERVICO)
admin.site.register(Usuario)
