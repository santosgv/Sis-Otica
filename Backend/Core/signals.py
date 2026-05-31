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

    entrada = Decimal(str(ordem.ENTRADA)) if ordem.ENTRADA else Decimal('0')

    total_parcelas_pagas = ordem.parcelas.filter(pago=True).aggregate(
        total=Sum('valor')
    )['total'] or Decimal('0')

    # VALOR_PAGO = sinal original + parcelas pagas
    novo_valor_pago = entrada + total_parcelas_pagas

    # Atualiza sem passar pelo HistoricalRecords (evita o erro do F() no INSERT)
    ORDEN.objects.filter(pk=ordem.pk).update(VALOR_PAGO=novo_valor_pago)

@receiver(post_save, sender=ORDEN)
def atualizar_valor_pago_ordem_sem_parcela(sender, instance, **kwargs):

    entrada = instance.ENTRADA or Decimal("0.00")

    # Evita save desnecessário
    if instance.VALOR_PAGO != entrada:

        ORDEN.objects.filter(id=instance.id).update(
            VALOR_PAGO=entrada
        )

        print("VALOR_PAGO atualizado")