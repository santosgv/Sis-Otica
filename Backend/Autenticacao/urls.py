from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    ColaboradorListView, ColaboradorDetailView, ColaboradorUpdateView,
    DescontoListView, DescontoDetailView, DescontoCreateView, DescontoUpdateView, DescontoDeleteView,
    ComissaoListView, ComissaoDetailView, ComissaoCreateView, ComissaoUpdateView, ComissaoDeleteView
)

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logar/', views.logar, name='logar'),
    path('sair/', views.sair, name="sair"),
    path('ativar_conta/<str:token>/', views.ativar_conta, name="ativar_conta"),
    path('alterar_conta', views.alterar_conta, name='alterar_conta'),
    path('listar_folha_pagamento/',views.listar_folha_pagamento, name='listar_folha_pagamento'),

        # Colaborador URLs
    path('colaboradores/', ColaboradorListView.as_view(), name='colaborador_list'),
    path('colaboradores/<int:pk>/', ColaboradorDetailView.as_view(), name='colaborador_detail'),
    path('colaboradores/<int:pk>/editar/', ColaboradorUpdateView.as_view(), name='colaborador_update'),

    # Desconto URLs
    path('descontos/', DescontoListView.as_view(), name='desconto_list'),
    path('descontos/<int:pk>/', DescontoDetailView.as_view(), name='desconto_detail'),
    path('descontos/novo/', DescontoCreateView.as_view(), name='desconto_create'),
    path('descontos/<int:pk>/editar/', DescontoUpdateView.as_view(), name='desconto_update'),
    path('descontos/<int:pk>/excluir/', DescontoDeleteView.as_view(), name='desconto_delete'),

    # Comissao URLs
    path('comissoes/', ComissaoListView.as_view(), name='comissao_list'),
    path('comissoes/<int:pk>/', ComissaoDetailView.as_view(), name='comissao_detail'),
    path('comissoes/novo/', ComissaoCreateView.as_view(), name='comissao_create'),
    path('comissoes/<int:pk>/editar/', ComissaoUpdateView.as_view(), name='comissao_update'),
    path('comissoes/<int:pk>/excluir/', ComissaoDeleteView.as_view(), name='comissao_delete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm_view.html"), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
    
]