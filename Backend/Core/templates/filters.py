from django import template
from Core.models import Produto

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