from decimal import Decimal

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum
from .models import Produto, AlertaEstoque,ParcelaOrdem, ORDEN

@receiver(post_save, sender=Produto)
def verificar_estoque_minimo(sender, instance, **kwargs):
    if instance.quantidade <= instance.quantidade_minima:
        mensagem = f"Atenção: O produto {instance.nome} está com estoque baixo ({instance.quantidade} unidades)."
        AlertaEstoque.objects.create(produto=instance, mensagem=mensagem)

@receiver(post_save, sender=ParcelaOrdem)
def atualizar_valor_pago_ordem(sender, instance, **kwargs):
    ordem = instance.ordem

    if instance.STATUS == 'C':
        return

    entrada = Decimal(str(ordem.ENTRADA.replace(".", "").replace(",", "."))) if ordem.ENTRADA else Decimal('0')

    total_parcelas_pagas = ordem.parcelas.filter(pago=True).aggregate(
        total=Sum('valor')
    )['total'] or Decimal('0')

    # VALOR_PAGO = sinal original + parcelas pagas
    novo_valor_pago = entrada + total_parcelas_pagas

    # Atualiza sem passar pelo HistoricalRecords (evita o erro do F() no INSERT)
    ORDEN.objects.filter(pk=ordem.pk).update(VALOR_PAGO=novo_valor_pago)

@receiver(post_save, sender=ORDEN)
def atualizar_valor_pago_ordem_sem_parcela(sender, instance, created, **kwargs):
    # Só executa na CRIAÇÃO — atualizações de status não devem resetar VALOR_PAGO
    if not created:
        return

    try:
        if instance.STATUS == 'C':
            return
        entrada_str = str(instance.ENTRADA or '0').replace(".", "").replace(",", ".")
        entrada = Decimal(entrada_str)
    except Exception:
        entrada = Decimal('0')

    # Só atualiza se VALOR_PAGO ainda estiver zerado (evita loop)
    if instance.VALOR_PAGO == Decimal('0'):
        ORDEN.objects.filter(id=instance.id).update(VALOR_PAGO=entrada)


@receiver(post_save, sender=ORDEN)
def cancela_parcela(sender, instance, created, **kwargs):
    # Só age em atualizações, não em criações
    if created:
        return

    if instance.STATUS == 'C':
        # Cancela todas as parcelas não pagas da ordem
        # Parcelas já pagas são mantidas intactas — o dinheiro já entrou no caixa
        instance.parcelas.filter(
            pago=False
        ).delete()