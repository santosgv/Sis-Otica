from django.contrib import admin
from Autenticacao.models import USUARIO,SALARIO,COMISSAO
from Core.models import CLIENTE,ORDEN,CAIXA,SERVICO,EMPRESA,Fornecedor,TipoUnitario,Produto,EntradaEstoque,SaidaEstoque,MovimentoEstoque,Tipo,Estilo



admin.site.register(CAIXA)
admin.site.register(COMISSAO)
admin.site.register(CLIENTE)
admin.site.register(SERVICO)
admin.site.register(ORDEN)
admin.site.register(USUARIO)
admin.site.register(SALARIO)
admin.site.register(EMPRESA)


admin.site.register(Fornecedor)
admin.site.register(TipoUnitario)
admin.site.register(Produto)
admin.site.register(EntradaEstoque)
admin.site.register(SaidaEstoque)
admin.site.register(MovimentoEstoque)
admin.site.register(Estilo)
admin.site.register(Tipo)