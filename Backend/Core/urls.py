
from django.urls import path
from django.conf import settings
from . import htmx_views
from django.conf.urls.static import static
from Core import views


app_name = 'Core'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro_cliente',views.cadastro_cliente,name='cadastro_cliente'),
    path('clientes',views.clientes,name='clientes'),
    path('cliente/<int:id>',views.Cliente,name='cliente'),
    path('Edita_cliente/<int:id>',views.Edita_cliente,name='Edita_cliente'),
    path('excluir_cliente/<int:id>',views.excluir_cliente,name='excluir_cliente'),
    path('Lista_Os',views.Lista_Os,name='Lista_Os'),
    path('Cadastrar_os/<int:id_cliente>',views.Cadastrar_os,name='Cadastrar_os'),
    path('Visualizar_os/<int:id_os>',views.Visualizar_os,name='Visualizar_os'),
    path('Editar_os/<int:id_os>',views.Editar_os,name='Editar_os'),
    path('Encerrar_os/<int:id_os>',views.Encerrar_os,name='Encerrar_os'),
    path('Cancelar_os/<int:id_os>',views.Cancelar_os,name='Cancelar_os'),
    path('Laboratorio_os/<int:id_os>',views.Laboratorio_os,name='Laboratorio_os'),
    path('Loja_os/<int:id_os>',views.Loja_os,name='Loja_os'),
    path('Imprimir_os/<int:id_os>',views.Imprimir_os, name='Imprimir_os'),
    path('Dashabord',views.Dashabord,name='Dashabord'),
    path('Caixa',views.Caixa, name='Caixa'),
    path('fechar_caixa',views.fechar_caixa, name='fechar_caixa'),
    path('cadastro_caixa',views.cadastro_caixa, name='cadastro_caixa'),
    path('vendas_ultimos_12_meses',views.vendas_ultimos_12_meses,name='vendas_ultimos_12_meses'),
    path('maiores_vendedores_30_dias',views.maiores_vendedores_30_dias,name='maiores_vendedores_30_dias'),
    path('transacoes_mensais',views.transacoes_mensais,name='transacoes_mensais'),
    path('obter_os_em_aberto',views.obter_os_em_aberto,name='obter_os_em_aberto'),
    path('relatorios',views.relatorios, name='relatorios'),
    path('dados_minhas_vendas',views.dados_minhas_vendas,name='dados_minhas_vendas'),
    path('dados_clientes',views.dados_clientes,name='dados_clientes'),
    path('minhas_vendas/',views.minhas_vendas, name='minhas_vendas'),
    path('receber',views.receber, name='receber'),
    path('obter_valores_registros_meses_anteriores',views.obter_valores_registros_meses_anteriores, name='obter_valores_registros_meses_anteriores'),
    path('caixa_mes_anterior',views.caixa_mes_anterior, name='caixa_mes_anterior'),
    path('estoque/',views.estoque, name='estoque'),
    path('produto_estoque/<int:id>',views.produto_estoque, name='produto_estoque'),

]

htmx_patterns =[
    path('search/',htmx_views.search, name='search'),
    path('search_cliente/',htmx_views.search_cliente,name='search_cliente'),
    path('all_estoque',htmx_views.all_estoque,name='all_estoque'),
    path('save_product',htmx_views.save_product, name='save_product'),

]

urlpatterns += htmx_patterns
