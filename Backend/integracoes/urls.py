
from django.urls import path
from .views import WhatsAppConfigView, WhatsAppDesconectarView, WhatsAppEnviarOsView, WhatsAppQRView, WhatsAppStatusView, WhatsAppStatusView, WhatsAppTesteView
from django_ratelimit.decorators import ratelimit


app_name = 'notificacoes'

urlpatterns = [
    path('whatsapp/',                        (WhatsAppConfigView.as_view()),        name='whatsapp_config'),
    path('whatsapp/qr/',                     (WhatsAppQRView.as_view()),            name='whatsapp_qr'),
    path('whatsapp/status/',                 (WhatsAppStatusView.as_view()),        name='whatsapp_status'),
    path('whatsapp/desconectar/',            (WhatsAppDesconectarView.as_view()),   name='whatsapp_desconectar'),
    path('whatsapp/teste/',                  (WhatsAppTesteView.as_view()),         name='whatsapp_teste'),
    path('os/<int:pk>/enviar/<str:tipo>/',   (WhatsAppEnviarOsView.as_view()), name='enviar_os'),
]