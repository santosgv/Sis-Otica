from django.contrib import admin
from Unidades.models import CLIENTE, CUSTO, LONGE, PERTO, UNIDADE
from Autenticacao.models import USUARIO,COMISSAO , ORDEN


admin.site.register(UNIDADE)
admin.site.register(CUSTO)
admin.site.register(COMISSAO)
admin.site.register(LONGE)
admin.site.register(PERTO)
admin.site.register(CLIENTE)

admin.site.register(ORDEN)
admin.site.register(USUARIO)
