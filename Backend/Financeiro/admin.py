from django.contrib import admin
from .models import (
    ContaFinanceira, CategoriaFinanceira, CentroCusto,
    ContaPagar, ParcelaContaPagar, FechamentoCaixa,
)


@admin.register(ContaFinanceira)
class ContaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'saldo_inicial', 'ativa')
    list_filter = ('tipo', 'ativa')
    search_fields = ('nome',)


@admin.register(CategoriaFinanceira)
class CategoriaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'categoria_pai', 'ativa')
    list_filter = ('tipo', 'ativa')
    search_fields = ('nome',)


@admin.register(CentroCusto)
class CentroCustoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)


class ParcelaContaPagarInline(admin.TabularInline):
    model = ParcelaContaPagar
    extra = 0


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'fornecedor', 'valor_total', 'status', 'data_emissao')
    list_filter = ('status', 'recorrente')
    search_fields = ('descricao',)
    inlines = [ParcelaContaPagarInline]


@admin.register(FechamentoCaixa)
class FechamentoCaixaAdmin(admin.ModelAdmin):
    list_display = ('conta', 'data', 'status', 'saldo_abertura', 'saldo_esperado',
                     'saldo_contado', 'diferenca')
    list_filter = ('status', 'conta')