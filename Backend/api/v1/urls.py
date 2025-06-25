from django.urls import include, path
from ..routers import router
from .viewsets import KanbanAPIView,UpdateCardStatusAPIView
from Core.views import (vendas_ultimos_12_meses,maiores_vendedores_30_dias,maiores_vendedores_meses,
                        transacoes_mensais,obter_os_em_aberto,dados_minhas_vendas,dados_clientes,
                        receber
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('', include(router.urls)),
    #path('dashboard/', RelatorioApiView.as_view(), name='api-dashboard'),
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
    
    # vendas por vendedor logado
    path('minhas_vendas_mes_atual',dados_minhas_vendas,name='minhas_vendas_mes_atual'),
    # essa view espera um renge de data inicio e fim.
    path('maiores_vendedores_meses',maiores_vendedores_meses,name='maiores_vendedores_meses'),
]