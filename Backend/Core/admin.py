from django.contrib import admin
from Autenticacao.models import USUARIO
from Core.models import (Review,LABORATORIO,CLIENTE,ORDEN,CAIXA,SERVICO,Fornecedor,
                         TipoUnitario,Produto,EntradaEstoque,SaidaEstoque,MovimentoEstoque,
                         Tipo,Estilo,AlertaEstoque,ParcelaOrdem,NotaFiscal)



admin.site.register(CAIXA)
admin.site.register(LABORATORIO)
admin.site.register(NotaFiscal)
admin.site.register(CLIENTE)
admin.site.register(SERVICO)
admin.site.register(ORDEN)
admin.site.register(ParcelaOrdem)
admin.site.register(USUARIO)
admin.site.register(Review)


admin.site.register(Fornecedor)
admin.site.register(TipoUnitario)
admin.site.register(Produto)
admin.site.register(EntradaEstoque)
admin.site.register(SaidaEstoque)
admin.site.register(AlertaEstoque)
admin.site.register(Estilo)
admin.site.register(Tipo)


@admin.register(MovimentoEstoque)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo', 'quantidade', 'data',)