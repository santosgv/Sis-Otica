from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Unidades import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro_cliente',views.cadastro_cliente,name='cadastro_cliente'),
    path('clientes',views.clientes,name='clientes'),
    path('cliente/<int:id>',views.Cliente,name='cliente'),
    path('Edita_cliente/<int:id>',views.Edita_cliente,name='Edita_cliente'),
    path('excluir_cliente/<int:id>',views.excluir_cliente,name='excluir_cliente'),
    path('Lista_Os',views.Lista_Os,name='Lista_Os'),
    path('Cadastrar_os',views.Cadastrar_os,name='Cadastrar_os')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)