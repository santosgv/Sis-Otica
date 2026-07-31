from decimal import Decimal,InvalidOperation

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum
from .models import Produto, AlertaEstoque,ParcelaOrdem, ORDEN
from .utils import parse_decimal

@receiver(post_save, sender=Produto)
def verificar_estoque_minimo(sender, instance, **kwargs):
    if instance.quantidade <= instance.quantidade_minima:
        mensagem = f"Atenção: O produto {instance.nome} está com estoque baixo ({instance.quantidade} unidades)."
        AlertaEstoque.objects.create(produto=instance, mensagem=mensagem)

@receiver(post_save, sender=ParcelaOrdem)
def atualizar_valor_pago_ordem(sender, instance, created, **kwargs):


    if instance.ordem.STATUS == 'C':
        return

    entrada = parse_decimal(instance.ordem.ENTRADA)

    total_parcelas_pagas = instance.ordem.parcelas.filter(pago=True).aggregate(
        total=Sum('valor')
    )['total'] or Decimal('0')

    novo_valor_pago = entrada + total_parcelas_pagas

    ORDEN.objects.filter(id=instance.ordem.id).update(
    VALOR_PAGO=novo_valor_pago
    )



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