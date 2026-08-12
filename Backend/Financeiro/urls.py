from django.urls import path
from . import views

app_name = 'Financeiro'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('contas-a-receber/', views.contas_a_receber, name='contas_a_receber'),
    path('contas-a-receber/<int:parcela_id>/receber/', views.receber_parcela_view,
         name='receber_parcela'),

    path('contas-a-pagar/', views.contas_a_pagar, name='contas_a_pagar'),
    path('contas-a-pagar/nova/', views.nova_conta_pagar, name='nova_conta_pagar'),
    path('contas-a-pagar/<int:parcela_id>/pagar/', views.pagar_parcela_view,
         name='pagar_parcela'),

    path('caixa/', views.caixa, name='caixa'),
    path('caixa/abrir/', views.abrir_caixa_view, name='abrir_caixa'),
    path('caixa/<int:fechamento_id>/fechar/', views.fechar_caixa_view, name='fechar_caixa'),
    path('caixa/sangria/', views.sangria_view, name='sangria'),
    path('caixa/suprimento/', views.suprimento_view, name='suprimento'),
]