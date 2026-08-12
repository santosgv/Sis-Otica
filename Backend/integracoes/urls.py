
from django.urls import path
from .views import WhatsAppConfigView, WhatsAppDesconectarView, WhatsAppEnviarOsView, WhatsAppQRView, WhatsAppStatusView, WhatsAppStatusView, WhatsAppTesteView
from django_ratelimit.decorators import ratelimit


app_name = 'notificacoes'

urlpatterns = [
    path('whatsapp/',ratelimit(key='ip', method='GET', rate='10/m')                   (WhatsAppConfigView.as_view()),        name='whatsapp_config'),
    path('whatsapp/qr/',ratelimit(key='ip', method='GET', rate='10/m')                (WhatsAppQRView.as_view()),            name='whatsapp_qr'),
    path('whatsapp/status/',ratelimit(key='ip', method='GET', rate='10/m')            (WhatsAppStatusView.as_view()),        name='whatsapp_status'),
    path('whatsapp/desconectar/',ratelimit(key='ip', method='GET', rate='10/m')       (WhatsAppDesconectarView.as_view()),   name='whatsapp_desconectar'),
    path('whatsapp/teste/',ratelimit(key='ip', method='GET', rate='10/m')             (WhatsAppTesteView.as_view()),         name='whatsapp_teste'),
    path('os/<int:pk>/enviar/<str:tipo>/', WhatsAppEnviarOsView.as_view(), name='enviar_os'),
]