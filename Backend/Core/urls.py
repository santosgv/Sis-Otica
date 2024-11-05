
from django.urls import path
from . import htmx_views
from .utils import Imprimir_os,export_clientes,export_os,create_pdf,gerar_relatorio_estoque_conferido
from Core import views
from django.contrib.auth import views as auth_views

from .views import (
    FornecedorListView,
    FornecedorDetailView,
    FornecedorCreateView,
    FornecedorUpdateView,
    FornecedorDeleteView,
    ServicoListView,
    ServicoCreateView,
    TipoUnitarioListView,
    TipoUnitarioCreateView,
    TipoUnitarioDetailView,
    TipoUnitarioUpdateView,
    TipoUnitarioDeleteView,
    EstiloListView,
    EstiloCreateView,
    EstiloDetailView,
    EstiloUpdateView,
    EstiloDeleteView,
    TipoListView,
    TipoCreateView,
    TipoDetailView,
    TipoUpdateView,
    TipoDeleteView
)


app_name = 'Core'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro_cliente',views.cadastro_cliente,name='cadastro_cliente'),
    path('fechar_card/', views.fechar_card, name='fechar_card'),
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
    path('Imprimir_os/<int:id_os>',Imprimir_os, name='Imprimir_os'),
    path('export_clientes',export_clientes,name='export_clientes'),
    path('export_os',export_os,name='export_os'),
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
    path('maiores_vendedores_meses',views.maiores_vendedores_meses, name='maiores_vendedores_meses'),
    path('relatorio_mes_anterior', views.relatorio_mes_anterior, name='relatorio_mes_anterior'),
    path('estoque/',views.estoque, name='estoque'),
    path('relatorio_estoque_conferido/',gerar_relatorio_estoque_conferido, name='relatorio_estoque_conferido'),
    path('produto_estoque/<int:id>',views.produto_estoque, name='produto_estoque'),
    path('realizar_entrada/',views.realizar_entrada_view,name='realizar_entrada'),
    path('realizar_saida_view/<int:id>',views.realizar_saida_view , name='realizar_saida'),
    path('editar_produto/<int:id>',views.editar_produto,name='editar_produto'),
    path('create_pdf/<str:codigo>/<int:quantidade>/', create_pdf, name='create_pdf'),
    path('entradas_estoque/', views.entradas_estoque,name='entradas_estoque'),
    path('saidas_estoque/', views.saidas_estoque,name='saidas_estoque'),
    path('movimentacao/',views.movimentacao,name='movimentacao'),
    path('vendas/',views.vendas, name='vendas'),



    path('fornecedores/', FornecedorListView.as_view(), name='fornecedor_list'),
    path('fornecedor/<int:pk>/', FornecedorDetailView.as_view(), name='fornecedor_detail'),
    path('fornecedor/novo/', FornecedorCreateView.as_view(), name='fornecedor_create'),
    path('fornecedor/<int:pk>/editar/', FornecedorUpdateView.as_view(), name='fornecedor_update'),
    path('fornecedor/<int:pk>/excluir/', FornecedorDeleteView.as_view(), name='fornecedor_delete'),
    path('servicos/',ServicoListView.as_view(),name='os_list'),
    path('servico/novo/', ServicoCreateView.as_view(), name='servico_create'),

    path('tiposund/', TipoUnitarioListView.as_view(), name='tiposund_list'),
    path('tipound/novo/', TipoUnitarioCreateView.as_view(), name='tipound_create'),
    path('tipound/<int:pk>/', TipoUnitarioDetailView.as_view(), name='tipound_detail'),
    path('tipound/<int:pk>/editar/', TipoUnitarioUpdateView.as_view(), name='tipound_update'),
    path('tipound/<int:pk>/excluir/', TipoUnitarioDeleteView.as_view(), name='tipound_delete'),

    path('estilos/', EstiloListView.as_view(), name='estilos_list'),
    path('estilo/novo/', EstiloCreateView.as_view(), name='estilo_create'),
    path('estilo/<int:pk>/', EstiloDetailView.as_view(), name='estilo_detail'),
    path('estilo/<int:pk>/editar/', EstiloUpdateView.as_view(), name='estilo_update'),
    path('estilo/<int:pk>/excluir/', EstiloDeleteView.as_view(), name='estilo_delete'),

    path('tipos/', TipoListView.as_view(), name='tipos_list'),
    path('tipo/novo/', TipoCreateView.as_view(), name='tipo_create'),
    path('tipo/<int:pk>/', TipoDetailView.as_view(), name='tipo_detail'),
    path('tipo/<int:pk>/editar/', TipoUpdateView.as_view(), name='tipo_update'),
    path('tipo/<int:pk>/excluir/', TipoDeleteView.as_view(), name='tipo_delete'),
]

htmx_patterns =[
    path('search/',htmx_views.search, name='search'),
    path('search_cliente/',htmx_views.search_cliente,name='search_cliente'),
    path('search_products/', htmx_views.search_products, name='search_products'),
    path('search_caixa/',htmx_views.search_caixa, name='search_caixa'),
    path('all_estoque',htmx_views.all_estoque,name='all_estoque'),
    path('save_product',htmx_views.save_product, name='save_product'),

]

urlpatterns += htmx_patterns
