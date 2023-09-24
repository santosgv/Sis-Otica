
from django.urls import path
from django.conf import settings
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
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)