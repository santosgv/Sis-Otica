from django import template
from Core.models import Produto
from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()

@register.filter(name='get_fornecedor')
def get_fornecedor(produto):
    fornecedor = Produto.objects.filter(fornecedor=produto.fornecedor)
    return fornecedor

@register.filter
def remove_formatacao_telefone(value):
    if not value:
        return ""
    return value.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")

@register.filter
def money(value):
    """
    Formata qualquer valor monetário corretamente.

    Exemplos:
    100 -> 100,00
    100.00 -> 100,00
    '100.00' -> 100,00
    '100,00' -> 100,00
    Decimal('1500.90') -> 1.500,90
    """

    if value in [None, "", "N/D"]:
        return "0,00"

    try:
        if isinstance(value, str):

            # Se já veio no padrão brasileiro
            if "," in value:
                value = value.replace(".", "").replace(",", ".")

            # Se veio no padrão python/sql (100.00)
            else:
                value = value.strip()

        valor = Decimal(str(value))

        return (
            f"{valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    except (InvalidOperation, ValueError, TypeError):
        return "0,00"