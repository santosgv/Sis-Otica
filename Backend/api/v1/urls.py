from django.urls import include, path
from ..routers import router
from Core.utils import gerar_relatorio_estoque_conferido,export_os,export_clientes,Imprimir_os,create_pdf
from .viewsets import (KanbanAPIView,UpdateCardStatusAPIView,FechamentoCaixaAPIView,
                        DadosCaixaAPIView,MinhasVendasAPIView,LojaOsAPIView,
                        EncerrarOsAPIView,EntregueOsAPIView,CanceladoOsAPIView,LaboratorioOsAPIView,
                        PedidosDoVendedorAPIView,DadosCaixaAnteriorApiView,FolhaPagamentoAPIView,
                        ComissaoViewSet,DescontoViewSet)
from Core.views import (vendas_ultimos_12_meses,maiores_vendedores_30_dias,maiores_vendedores_meses,
                        transacoes_mensais,obter_os_em_aberto,dados_minhas_vendas,dados_clientes,
                        receber,fechar_caixa
)

from api.views import baixar_pdf,search_products_api,realizar_saida_api

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('', include(router.urls)),
    path('kanban/',KanbanAPIView.as_view(),name='kanban'),
    path('cards/<int:card_id>/update-status/', UpdateCardStatusAPIView.as_view(), name='update-card-status'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('vendas_ultimos_12_meses',vendas_ultimos_12_meses,name='vendas_ultimos_12_meses'),
    path('maiores_vendedores_30_dias',maiores_vendedores_30_dias,name='maiores_vendedores_30_dias'),
    path('caixa_transacoes_mensais',transacoes_mensais,name='caixa_transacoes_mensais'),
    path('obter_os_em_aberto',obter_os_em_aberto,name='obter_os_em_aberto'),
    path('total_clientes_ativos',dados_clientes,name='total_clientes_ativos'),
    path('total_vendido_hoje',receber,name='total_vendido_hoje'),

    # fechamento caixa
    path('fechamento-caixa/', FechamentoCaixaAPIView.as_view(), name='fechamento-caixa'),
    path('caixa_anterior/',DadosCaixaAnteriorApiView.as_view(), name='caixa_anterior'),
    path('dados-caixa/', DadosCaixaAPIView.as_view(), name='dados-caixa'),
    
    # vendas por vendedor logado
    path('minhas_vendas_mes_atual',MinhasVendasAPIView.as_view(),name='minhas_vendas_mes_atual'),
    path("pedidos_vendedor/", PedidosDoVendedorAPIView.as_view(), name="pedidos_vendedor"),

    # folha pagamento
    path('folha/<int:usuario_id>/<str:referencia>/', FolhaPagamentoAPIView.as_view(), name='folha_pagamento'),

    # htmx
    path('search_products/', search_products_api, name='search_products_api'),
    path('realizar_saida_api/', realizar_saida_api, name='realizar_saida_api'),


    # botoes
    path('baixar_pdf/<int:colaborador_id>/<str:referencia>/',baixar_pdf,name='baixar_pdf'),
    path('gerar_relatorio_estoque_conferido',gerar_relatorio_estoque_conferido ,name='gerar_relatorio_estoque_conferido'),
    path('imprimir_os/<int:id_os>/',Imprimir_os,name='imprimir_os'),
    path("loja_os/<int:id_os>/", LojaOsAPIView.as_view(), name="loja_os"),
    path("encerrar_os/<int:id_os>/", EncerrarOsAPIView.as_view(), name="encerrar_os"),
    path("cancelar_os/<int:id_os>/", CanceladoOsAPIView.as_view(), name="cancelar_os"),
    path("entregar_os/<int:id_os>/", EntregueOsAPIView.as_view(), name="entregar_os"),
    path("laboratorio_os/<int:id_os>/", LaboratorioOsAPIView.as_view(), name="laboratorio_os"),
    path('export_os',export_os,name='export_os'),
    path('export_clientes',export_clientes,name='export_clientes'),
    path('etiquetas/<str:codigo>/<int:quantidade>/',create_pdf,name='etiquetas'),
    path('fechar_caixa',fechar_caixa,name='fechar_caixa')

]