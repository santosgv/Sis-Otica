import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class WhatsAppConfigError(Exception):
    pass


class WhatsAppAPIError(Exception):
    pass


def _base_url() -> str:
    return getattr(settings, 'EVOLUTION_API_URL', 'http://localhost:8080').rstrip('/')


def _api_key() -> str:
    """Obtém a API Key da Evolution API."""
    api_key = getattr(settings, 'EVOLUTION_API_KEY', '')
    if not api_key:
        raise WhatsAppConfigError(
            "EVOLUTION_API_KEY não configurada no settings.py ou .env"
        )

    return api_key


def _headers() -> dict:
    return {
        'apikey':       _api_key(),
        'Content-Type': 'application/json',
    }


def _req(method: str, path: str, json=None, timeout=10) -> dict:
    """Requisição à Evolution API com tratamento de erro unificado."""
    url = f'{_base_url()}{path}'
    try:
        r = getattr(requests, method)(url, headers=_headers(), json=json, timeout=timeout)
    except requests.exceptions.ConnectionError:
        raise WhatsAppAPIError(
            "Evolution API indisponível. "
            "Verifique se o Docker está rodando: docker compose up -d"
        )
    except requests.exceptions.Timeout:
        raise WhatsAppAPIError("Timeout ao conectar com a Evolution API.")

    try:
        data = r.json()
    except Exception:
        data = {'detail': r.text}

    if not r.ok:
        detalhe = data.get('message') or data.get('detail') or str(data)
        raise WhatsAppAPIError(f"Evolution API [{r.status_code}]: {detalhe}")

    return data


# ── Gerenciamento de instância ────────────────────────────────

def criar_instancia(instance_name: str) -> dict:
    """Cria instância na Evolution API. Cada empresa tem a sua."""
    return _req('post', '/instance/create', json={
        'instanceName': instance_name,
        'qrcode':       True,
        'integration':  'WHATSAPP-BAILEYS',
    })


def status_instancia(instance_name: str) -> dict:
    """
    Retorna estado da instância.
    state: 'open' = conectado | 'close' = desconectado | 'connecting' = aguardando QR
    """
    try:
        return _req('get', f'/instance/connectionState/{instance_name}')
    except WhatsAppAPIError:
        return {'instance': {'state': 'close'}}


def gerar_qr(instance_name: str) -> dict:
    """Gera/renova QR code. Retorna dict com 'base64' e 'code'."""
    return _req('get', f'/instance/connect/{instance_name}')


def desconectar_instancia(instance_name: str) -> dict:
    """Desconecta o número mas mantém a instância."""
    return _req('delete', f'/instance/logout/{instance_name}')


def deletar_instancia(instance_name: str) -> dict:
    """Remove completamente a instância."""
    return _req('delete', f'/instance/delete/{instance_name}')


def listar_instancias() -> list:
    try:
        data = _req('get', '/instance/fetchInstances')
        return data if isinstance(data, list) else []
    except WhatsAppAPIError:
        return []


def instancia_existe(instance_name: str) -> bool:
    nomes = [
        i.get('instance', {}).get('instanceName', '')
        for i in listar_instancias()
    ]
    return instance_name in nomes


def obter_ou_criar_instancia(instance_name: str) -> dict:
    """Garante que a instância existe, criando se necessário."""
    if not instancia_existe(instance_name):
        logger.info(f"Criando instância Evolution API: {instance_name}")
        criar_instancia(instance_name)
    return status_instancia(instance_name)


# ── Envio de mensagens ────────────────────────────────────────

def _formatar_telefone(telefone: str) -> str:
    """'(11) 99999-8888' → '5511999998888'"""
    numeros = ''.join(filter(str.isdigit, telefone))
    if not numeros.startswith('55'):
        numeros = f'55{numeros}'
    return numeros


def enviar_texto(instance_name: str, telefone: str, mensagem: str,delay: int = 1000, presence: str = "composing") -> dict:
    """Envia mensagem de texto. Suporta *negrito* e _itálico_ do WhatsApp."""
    numero = _formatar_telefone(telefone)
    payload = {
        "number": numero,
        "textMessage": {
            "text": mensagem
        },
        "options": {
            "delay": delay,
            "presence": presence,
            "linkPreview": True
        }
    }
    logger.info(f"📨 Enviando mensagem para {numero} via {instance_name}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        data = _req('post', f'/message/sendText/{instance_name}', json=payload)
        logger.info(f"✅ Mensagem enviada com sucesso para {numero}")
        return data
    except WhatsAppAPIError as e:
        logger.error(f"❌ Erro ao enviar mensagem: {str(e)}")
        raise


# ── Mensagens do domínio ──────────────────────────────────────

def _telefone(orden) -> str:
    tel = getattr(orden.CLIENTE, 'TELEFONE', '') or ''
    if not tel:
        raise WhatsAppConfigError(
            f"Cliente '{orden.CLIENTE.TELEFONE}' não tem telefone cadastrado."
        )
    return tel



def notificar_os_criada(instance_name: str, ordem) -> dict:
    valor_formatado = f"R$ {ordem.VALOR:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    lentes = ordem.LENTES if ordem.LENTES != 'N/D' else 'não informado'
    montagem = ordem.MONTAGEM if ordem.MONTAGEM != 'N/D' else 'não informado'
    armacao = ordem.ARMACAO if ordem.ARMACAO != 'N/D' else 'não informado'

    msg = (
        f"✅ *Compra Confirmada!*\n\n"
        f"Olá, {ordem.CLIENTE.NOME}! Seu pedido foi recebido com sucesso.\n"
        f"🔹 *Nº do Pedido:* #{ordem.pk}\n"
        f"🔹 *Serviço:* {ordem.SERVICO.SERVICO}\n"
        f"🔹 *Lentes:* {lentes}\n"
        f"🔹 *Montagem:* {montagem}\n"
        f"🔹 *Armação:* {armacao}\n\n"
        f"📅 *Previsão de Entrega:* {ordem.PREVISAO_ENTREGA.strftime('%d/%m/%Y')}\n"
        f"💰 *Valor Total:* {valor_formatado}\n"
        f"💳 *Forma de Pagamento:* {ordem.get_FORMA_PAG_display()}\n\n"
        f"📌 *Próximos passos:*\n"
        f"• Acompanhe o status pelo nosso sistema\n"
        f"• Quando pronto, avisaremos você\n"
        f"• Compareça à nossa loja para retirada\n"
        f"• Traga um documento de identificação\n\n"
        f"🤝 Agradecemos pela confiança!\n"
        f"*Ótica {settings.UNIDADE}* – Cuidando da sua visão"
    )
    print(msg)
    #return enviar_texto(instance_name, _telefone(ordem), msg)

def notificar_os_entregue(instance_name: str, ordem) -> dict:
    msg = (
        f"🎉 *Pedido Entregue!*\n\n"
        f"Olá, {ordem.CLIENTE.NOME}!\n"
        f"Seu pedido *#{ordem.pk}* foi retirado com sucesso.\n\n"
        f"Esperamos que esteja satisfeito com seus novos óculos! 😊\n\n"
        f"📝 *Sua opinião é importante:*\n"
        f"Gostaríamos de saber como foi sua experiência. Responda com um simples:\n"
        f"• 👍 (ótimo)  • 😊 (bom)  • 😐 (regular)  • 👎 (ruim)\n\n"
        f"Se preferir, deixe um comentário no nosso site.\n\n"
        f"*Cuide bem da sua visão!* 👁️\n"
        f"*Ótica {settings.UNIDADE}*"
    )
    print(msg)
    #return enviar_texto(instance_name, _telefone(ordem), msg)

def notificar_troca_status(instance_name: str, ordem, status_novo) -> dict:
    status_legenda = {
        'L': 'em produção no laboratório',
        'J': 'pronto para retirada',
    }
    descricao = status_legenda.get(status_novo, status_novo)

    if descricao == 'em produção no laboratório':
        msg = (
            f"🔄 *Atualização do Pedido #{ordem.pk}*\n\n"
            f"Olá, {ordem.CLIENTE.NOME}!\n"
            f"Seu pedido agora está *{descricao}*.\n\n"
            f"📅 *Previsão de Entrega:* {ordem.PREVISAO_ENTREGA.strftime('%d/%m/%Y')}\n\n"
            f"Fique atento! Em breve enviaremos mais novidades.\n"
            f"😊 Equipe Ótica {settings.UNIDADE}"
        )
        print(msg)
        #return enviar_texto(instance_name, _telefone(ordem), msg)
    if descricao == 'pronto para retirada':
        msg = (
        f"🎉 *Pedido Pronto para Retirada!*\n\n"
        f"Olá, {ordem.CLIENTE.NOME}!\n"
        f"Seu pedido *#{ordem.pk}* já está disponível na nossa loja.\n\n"
        f"📅 *Previsão de Entrega:* {ordem.PREVISAO_ENTREGA.strftime('%d/%m/%Y')}\n"
        f"💰 *Valor:* R$ {ordem.VALOR:.2f}".replace('.', ',') + "\n\n"
        f"📌 *Para retirar, não se esqueça:*\n"
        f"• Traga um documento de identificação com foto\n"
        f"• Apresente este número de pedido\n\n"
        f"😊 Estamos ansiosos para vê-lo!\n"
        f"*Ótica {settings.UNIDADE}* – Cuidando da sua visão")
        print(msg)
        #return enviar_texto(instance_name, _telefone(ordem), msg)

def notificar_cancelamento(instance_name: str, ordem) -> dict:
    msg = (
        f"❌ *Pedido Cancelado*\n\n"
        f"Olá, {ordem.CLIENTE.NOME}!\n"
        f"Seu pedido *#{ordem.pk}* foi cancelado.\n\n"
        f"📌 *Motivo do cancelamento:*\n"
        f"• Solicitação do cliente\n"
        f"• Indisponibilidade de itens\n"
        f"• Problemas com pagamento\n"
        f"• Outros motivos operacionais\n"
        f"Lamentamos o ocorrido. Estamos à disposição para ajudar! 💙\n"
        f"😊 Equipe Ótica {settings.UNIDADE}"

    )
    print(msg)
    #return enviar_texto(instance_name, _telefone(ordem), msg)

def mensagem_lembrete_anual(instance_name: str, ordem)-> dict:
    msg = (
        f"👁️ *Hora de cuidar da sua visão!*\n\n"
        f"Olá, {ordem.CLIENTE.NOME}!\n"
        f"Já faz mais de um ano desde seu último exame de vista.\n"
        f"Agende uma consulta conosco e garanta que seus óculos estão\n"
        f"atualizados para o seu dia a dia.\n\n"
        f"responda esta mensagem para agendar.\n\n"
        f"*Sua visão merece o melhor!* 😉\n"
        f"*Ótica {settings.UNIDADE}*"
    )
    print(msg)
    #return enviar_texto(instance_name, _telefone(ordem), msg)