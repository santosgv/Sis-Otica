import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView
from Core.models import ORDEN
from .models import WhatsAppConfig
from .service import (
    WhatsAppAPIError, WhatsAppConfigError,
    criar_instancia, gerar_qr, status_instancia,
    desconectar_instancia, deletar_instancia,
    instancia_existe, enviar_texto,
    notificar_os_criada, notificar_os_entregue,
    notificar_troca_status,mensagem_lembrete_anual, notificar_cancelamento,
)

logger = logging.getLogger(__name__)


def _instance_name(empresa) -> str:
    """Gera nome único de instância para a empresa."""
    return f'SGO_{empresa}'


# ─────────────────────────────────────────────────────────────
# PÁGINA PRINCIPAL — configuração e painel
# ─────────────────────────────────────────────────────────────

class WhatsAppConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'notificacoes/whatsapp_config.html'

    def get_context_data(self, **kwargs):
        ctx     = super().get_context_data(**kwargs)
        config  = WhatsAppConfig.objects.first()
        ctx['config']  = config

        return ctx

    def post(self, request):

        acao = request.POST.get('acao')

        if acao == 'conectar':
            return self._conectar(request)

        if acao == 'salvar_preferencias':
            return self._salvar_preferencias(request)

        messages.error(request, 'Ação inválida.')
        return redirect('notificacoes:whatsapp_config')

    @staticmethod
    def _conectar(request):
        """Cria a instância na Evolution API e inicia o fluxo de QR."""
        instance_name = _instance_name('Sis-Otica')  # Substitua pelo nome da empresa real

        try:
            # Cria instância se não existir
            if not instancia_existe(instance_name):
                criar_instancia(instance_name)

            # Cria ou atualiza config local
            config, criado = WhatsAppConfig.objects.get_or_create(
                defaults={'instance_name': instance_name},
            )
            if not criado:
                config.instance_name = instance_name
                config.ativo = True
                config.save(update_fields=['instance_name', 'ativo'])

            messages.success(request, 'Instância criada! Escaneie o QR Code abaixo com seu celular.')
            return redirect('notificacoes:whatsapp_qr')

        except WhatsAppAPIError as e:
            messages.error(request, f'Erro ao conectar: {e}')
            return redirect('notificacoes:whatsapp_config')

    @staticmethod
    def _salvar_preferencias(request):
        config = WhatsAppConfig.objects.first()
        if not config:
            messages.error(request, 'Configure o WhatsApp primeiro.')
            return redirect('notificacoes:whatsapp_config')

        config.notif_os_criada           = 'notif_os_criada'        in request.POST
        config.notif_troca_status        = 'notif_troca_status'     in request.POST
        config.notif_os_entregue         = 'notif_os_entregue'      in request.POST
        config.notif_cancelamento        = 'notif_cancelamento'     in request.POST
        config.notif_lembrete_anual      = 'notif_lembrete_anual'   in request.POST
        config.save(update_fields=[
            'notif_os_criada', 'notif_troca_status',
            'notif_os_entregue', 'notif_cancelamento', 'notif_lembrete_anual',
        ])
        messages.success(request, 'Preferências salvas.')
        return redirect('notificacoes:whatsapp_config')


# ─────────────────────────────────────────────────────────────
# QR CODE — exibe o QR para escanear
# ─────────────────────────────────────────────────────────────

class WhatsAppQRView(LoginRequiredMixin, View):

    def get(self, request):
        config  = WhatsAppConfig.objects.first()

        if not config:
            messages.error(request, 'Configure o WhatsApp primeiro.')
            return redirect('notificacoes:whatsapp_config')

        # Se já está conectado, vai para o painel
        if config.esta_conectado:
            messages.success(request, 'WhatsApp já está conectado!')
            return redirect('notificacoes:whatsapp_config')

        qr_data   = None
        qr_base64 = None
        erro      = None

        try:
            data      = gerar_qr(config.instance_name)
            qr_base64 = data.get('base64') or data.get('qrcode', {}).get('base64')
            qr_data   = data.get('code')   or data.get('qrcode', {}).get('code')
        except WhatsAppAPIError as e:
            erro = str(e)

        return render(request, 'notificacoes/whatsapp_qr.html', {
            'config':    config,
            'qr_base64': qr_base64,
            'qr_data':   qr_data,
            'erro':      erro,
        })


# ─────────────────────────────────────────────────────────────
# STATUS — polling AJAX da página de QR
# ─────────────────────────────────────────────────────────────

class WhatsAppStatusView(LoginRequiredMixin, View):
    """Retorna JSON com o estado atual da instância. Usado por polling JS."""

    def get(self, request):
        config  = WhatsAppConfig.objects.first()

        if not config:
            return JsonResponse({'estado': 'desconectado', 'conectado': False})

        try:
            data  = status_instancia(config.instance_name)
            state = data.get('instance', {}).get('state', 'close')
            phone = data.get('instance', {}).get('profileName', '')

            # Atualiza número vinculado se disponível
            if state == 'open' and phone and phone != config.numero_vinculado:
                config.numero_vinculado = phone
                config.save(update_fields=['numero_vinculado'])

            conectado = state == 'open'
            print(f"WhatsAppStatusView: estado={state}, conectado={conectado}, numero={config.numero_vinculado}, instancia ={config.instance_name}")
            return JsonResponse({
                'estado':    state,
                'conectado': conectado,
                'numero':    config.numero_vinculado,
            })

        except WhatsAppAPIError as e:
            return JsonResponse({'estado': 'erro', 'conectado': False, 'erro': str(e)})


# ─────────────────────────────────────────────────────────────
# DESCONECTAR
# ─────────────────────────────────────────────────────────────

class WhatsAppDesconectarView(LoginRequiredMixin, View):

    def post(self, request):
        config  = WhatsAppConfig.objects.first()

        if not config:
            messages.error(request, 'Nenhuma configuração encontrada.')
            return redirect('notificacoes:whatsapp_config')

        acao = request.POST.get('acao', 'logout')

        try:
            if acao == 'deletar':
                desconectar_instancia(config.instance_name)
                deletar_instancia(config.instance_name)
                config.delete()
                messages.warning(request, 'WhatsApp desconectado e instância removida.')
            else:
                desconectar_instancia(config.instance_name)
                config.numero_vinculado = ''
                config.save(update_fields=['numero_vinculado'])
                messages.warning(request, 'WhatsApp desconectado. Escaneie o QR para reconectar.')

        except WhatsAppAPIError as e:
            messages.error(request, f'Erro ao desconectar: {e}')

        return redirect('notificacoes:whatsapp_config')


# ─────────────────────────────────────────────────────────────
# ENVIO DE TESTE
# ─────────────────────────────────────────────────────────────

class WhatsAppTesteView(LoginRequiredMixin, View):
    """Envia mensagem de teste. Retorna JSON para AJAX."""

    def post(self, request):
        config   = WhatsAppConfig.objects.first()
        telefone = request.POST.get('telefone', '').strip()

        if not config:
            return JsonResponse({'ok': False, 'erro': 'WhatsApp não configurado.'})
        if not telefone:
            return JsonResponse({'ok': False, 'erro': 'Informe um telefone.'})
        if not config.esta_conectado:
            return JsonResponse({'ok': False, 'erro': 'WhatsApp não está conectado. Escaneie o QR code.'})

        try:
            enviar_texto(
                config.instance_name,
                telefone,
                '✅ *Teste SGO!*\n\nSua integração com o WhatsApp está funcionando. '
                'Você receberá notificações automáticas por este número.'
            )
            config.registrar_envio()
            return JsonResponse({'ok': True, 'mensagem': f'Mensagem enviada para {telefone}!'})

        except (WhatsAppConfigError, WhatsAppAPIError) as e:
            return JsonResponse({'ok': False, 'erro': str(e)})


# ─────────────────────────────────────────────────────────────
# ENVIO MANUAL POR OS
# ─────────────────────────────────────────────────────────────


# troca_status precisa do status atual como segundo argumento — os demais
# recebem só (instance_name, ordem). Normalizado aqui com lambdas para que
# todas as entradas do dicionário tenham a mesma assinatura de chamada.
FUNCOES_NOTIFICACAO = {
    'os_criada': lambda instance_name, ordem: notificar_os_criada(instance_name, ordem),
    'os_entregue': lambda instance_name, ordem: notificar_os_entregue(instance_name, ordem),
    'cancelamento': lambda instance_name, ordem: notificar_cancelamento(instance_name, ordem),
    'troca_status': lambda instance_name, ordem: notificar_troca_status(
        instance_name, ordem, ordem.STATUS
    ),
    'lembrete_anual': lambda instance_name, ordem: mensagem_lembrete_anual(instance_name, ordem),
}

class WhatsAppEnviarOsView(LoginRequiredMixin, View):
    """Envio manual (ou reenvio) de uma notificação para o cliente de uma OS.
 
    Útil como botão de "reenviar" na tela da OS quando o envio automático
    (Notificacoes/signals.py) falhou, ou para testar um tipo de mensagem
    específico independente do status atual da OS.
    """
 
    def post(self, request, pk, tipo):
        ordem = get_object_or_404(ORDEN, pk=pk)
 
        fn = FUNCOES_NOTIFICACAO.get(tipo)
        if fn is None:
            messages.error(request, f'Tipo de notificação inválido: "{tipo}".')
            return redirect('Core:Visualizar_os', id_os=pk)
 
        config = WhatsAppConfig.objects.filter(ativo=True).first()
 
        if not config:
            messages.error(
                request, 'WhatsApp não configurado. Acesse Configurações → WhatsApp.'
            )
            return redirect('Core:Visualizar_os', id_os=pk)
 
        if not config.esta_conectado:
            messages.error(request, 'WhatsApp não está conectado. Escaneie o QR code.')
            return redirect('Notificacoes:whatsapp_qr')
 
        try:
            fn(config.instance_name, ordem)
            config.registrar_envio()
            messages.success(request, f'✅ Mensagem enviada para {ordem.CLIENTE.NOME}!')
 
        except WhatsAppConfigError as e:
            messages.error(request, str(e))
        except WhatsAppAPIError as e:
            messages.error(request, f'Erro ao enviar: {e}')
 
        return redirect('Core:Visualizar_os', id_os=pk)