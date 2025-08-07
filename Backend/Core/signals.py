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

    # Soma das parcelas pagas
    total_pago = ordem.parcelas.filter(pago=True).aggregate(
        total=Sum('valor')
    )['total'] or 0

    # Atualiza o campo ENTRADA com o total pago
    ordem.ENTRADA = total_pago
    ordem.save(update_fields=['ENTRADA'])