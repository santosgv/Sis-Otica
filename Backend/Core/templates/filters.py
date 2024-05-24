from django import template
from Core.models import Produto

register = template.Library()

@register.filter(name='get_fornecedor')
def get_fornecedor(produto):
    fornecedor = Produto.objects.filter(fornecedor=produto.fornecedor)
    return fornecedor