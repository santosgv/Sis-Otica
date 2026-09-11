"""
Notificacoes/signals.py

Dispara os alertas de WhatsApp automaticamente quando uma ORDEN (Core) é
criada ou muda de status, respeitando os toggles de WhatsAppConfig.

Registrar em Notificacoes/apps.py (ver PATCH_apps.py incluído nesta entrega).
"""
import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from Core.models import ORDEN

from .models import WhatsAppConfig
from .service import (
    WhatsAppAPIError,
    WhatsAppConfigError,
    notificar_cancelamento,
    notificar_os_criada,
    notificar_os_entregue,
    notificar_troca_status,
)

logger = logging.getLogger(__name__)

# Status que disparam o alerta genérico de "troca de status"
# ('L' = em produção no laboratório, 'J' = pronto para retirada — mesmos
# valores usados em service.py:status_legenda)
STATUS_QUE_DISPARAM_TROCA_STATUS = {'L', 'J'}


@receiver(pre_save, sender=ORDEN)
def _capturar_status_anterior(sender, instance, **kwargs):
    """Guarda o STATUS que a OS tinha no banco ANTES deste save, na própria
    instância (`instance._status_anterior`), para o post_save conseguir
    detectar uma transição real de status — e não apenas o valor atual, que
    seria o mesmo em qualquer save subsequente com STATUS inalterado
    (edição de outros campos, por exemplo).

    Sem isso, salvar a OS por qualquer outro motivo com STATUS='E' já
    setado reenviaria o alerta de entrega toda vez.
    """
    if not instance.pk:
        instance._status_anterior = None
        return
    try:
        instance._status_anterior = (
            ORDEN.objects.only('STATUS').get(pk=instance.pk).STATUS
        )
    except ORDEN.DoesNotExist:
        instance._status_anterior = None


def _config_pronta_para_enviar(campo_toggle: str):
    """Retorna a WhatsAppConfig ativa, com o toggle pedido ligado e
    efetivamente conectada — ou None se qualquer uma dessas condições não
    for atendida. Nesse caso o alerta é simplesmente pulado (logado como
    aviso), nunca um erro que travaria o save da OS.
    """
    config = WhatsAppConfig.objects.filter(ativo=True).first()
    if not config:
        return None
    if not getattr(config, campo_toggle, False):
        return None
    if not config.esta_conectado:
        logger.warning(
            'Alerta WhatsApp (%s) pulado: instância "%s" não está conectada.',
            campo_toggle, config.instance_name,
        )
        return None
    return config


def _enviar_com_seguranca(fn, config, ordem, *args_extras):
    """Executa o envio isolando qualquer falha. O save da OS já aconteceu
    antes deste signal rodar — uma falha no WhatsApp (API fora do ar,
    cliente sem telefone, timeout) NUNCA deve aparecer como erro para quem
    só estava salvando a OS.
    """
    try:
        fn(config.instance_name, ordem, *args_extras)
        config.registrar_envio()
    except WhatsAppConfigError as e:
        # ex: cliente sem telefone cadastrado — aviso, não é uma falha de
        # infraestrutura
        logger.warning('Alerta WhatsApp não enviado (OS #%s): %s', ordem.pk, e)
    except WhatsAppAPIError as e:
        logger.error('Falha ao enviar alerta WhatsApp (OS #%s): %s', ordem.pk, e)
    except Exception:
        logger.exception(
            'Erro inesperado ao enviar alerta WhatsApp (OS #%s)', ordem.pk
        )


@receiver(post_save, sender=ORDEN)
def enviar_alertas_whatsapp(sender, instance, created, **kwargs):
    # --- OS recém-criada ---
    if created:
        config = _config_pronta_para_enviar('notif_os_criada')
        if config:
            _enviar_com_seguranca(notificar_os_criada, config, instance)
        return

    # --- Idempotência: só age se o STATUS realmente mudou neste save ---
    status_anterior = getattr(instance, '_status_anterior', None)
    status_atual = instance.STATUS
    if status_anterior == status_atual:
        return

    if status_atual == 'E':
        config = _config_pronta_para_enviar('notif_os_entregue')
        if config:
            _enviar_com_seguranca(notificar_os_entregue, config, instance)

    elif status_atual == 'C':
        config = _config_pronta_para_enviar('notif_cancelamento')
        if config:
            _enviar_com_seguranca(notificar_cancelamento, config, instance)

    elif status_atual in STATUS_QUE_DISPARAM_TROCA_STATUS:
        config = _config_pronta_para_enviar('notif_troca_status')
        if config:
            _enviar_com_seguranca(
                notificar_troca_status, config, instance, status_atual
            )

