"""Relatórios do módulo Financeiro (Fase 12 do prompt master).

Convenções seguidas em todo o módulo:
- Toda agregação usa `values().annotate()`/`aggregate()` do ORM — nenhum loop Python
  somando linha a linha (mesmo cuidado com N+1 da Fase 11).
- Datas de filtro são inclusivas nas duas pontas (`data_inicio <= x <= data_fim`).
"""
from decimal import Decimal
from datetime import timedelta

from django.db.models import Sum, Count
from django.utils.timezone import now

from Core.models import ParcelaOrdem

from .models import (
    MovimentoFinanceiro, ParcelaContaPagar, RecebimentoParcela,
    PagamentoParcelaContaPagar,
)


def _inicio_periodo(data, agrupamento):
    """Calcula o início do bucket (dia/semana/mês) ao qual `data` pertence.

    Implementado em Python sobre um conjunto pequeno de datas distintas
    (não por linha de movimento) para contornar uma incompatibilidade real
    entre `TruncWeek`/`TruncMonth`/`TruncDate` do Django e `DateField` (não
    `DateTimeField`) no backend SQLite com `USE_TZ=True`: o Django gera
    `django_datetime_cast_date(..., tz_origem, tz_destino)` mesmo para um
    campo que já é só data, e a função SQLite registrada quebra
    (`OperationalError: user-defined function raised exception`).
    Reproduzido isoladamente via `manage.py shell` durante a Fase 12.
    """
    if agrupamento == 'dia':
        return data
    if agrupamento == 'semana':
        return data - timedelta(days=data.weekday())
    if agrupamento == 'mes':
        return data.replace(day=1)
    raise ValueError(f'Agrupamento inválido: {agrupamento}')


# ---------------------------------------------------------------------------
# Fluxo de caixa realizado
# ---------------------------------------------------------------------------

def fluxo_caixa_realizado(data_inicio, data_fim, agrupamento='dia', conta=None):
    """Entradas/saídas efetivamente movimentadas no período, agrupadas por
    dia/semana/mês. Agrupamento exato por dia é feito no banco (uma query
    por direção); semana/mês são rebucketizados em Python sobre o pequeno
    conjunto de dias distintos já agregados — não por movimento individual.
    """
    if agrupamento not in ('dia', 'semana', 'mes'):
        raise ValueError(f'Agrupamento inválido: {agrupamento}')

    qs = MovimentoFinanceiro.objects.filter(data__gte=data_inicio, data__lte=data_fim)
    if conta is not None:
        qs = qs.filter(conta=conta)

    entradas_por_dia = (
        qs.filter(tipo__in=MovimentoFinanceiro.TIPOS_ENTRADA)
        .values('data').annotate(total=Sum('valor'))
    )
    saidas_por_dia = (
        qs.filter(tipo__in=MovimentoFinanceiro.TIPOS_SAIDA)
        .values('data').annotate(total=Sum('valor'))
    )

    buckets = {}
    for r in entradas_por_dia:
        chave = _inicio_periodo(r['data'], agrupamento)
        buckets.setdefault(chave, {'entradas': Decimal('0'), 'saidas': Decimal('0')})
        buckets[chave]['entradas'] += r['total']
    for r in saidas_por_dia:
        chave = _inicio_periodo(r['data'], agrupamento)
        buckets.setdefault(chave, {'entradas': Decimal('0'), 'saidas': Decimal('0')})
        buckets[chave]['saidas'] += r['total']

    resultado = []
    for periodo in sorted(buckets):
        e = buckets[periodo]['entradas']
        s = buckets[periodo]['saidas']
        resultado.append({
            'periodo': periodo, 'entradas': e, 'saidas': s, 'resultado': e - s,
        })
    return resultado


# ---------------------------------------------------------------------------
# Fluxo de caixa projetado
# ---------------------------------------------------------------------------

def fluxo_caixa_projetado(data_inicio, data_fim, agrupamento='dia'):
    """Contas a receber e a pagar em aberto, agrupadas por data de
    vencimento. Mesma estratégia de `fluxo_caixa_realizado`: agrupamento
    exato por dia no banco, rebucketizado em Python para semana/mês.
    """
    if agrupamento not in ('dia', 'semana', 'mes'):
        raise ValueError(f'Agrupamento inválido: {agrupamento}')

    parcelas_receber = ParcelaOrdem.objects.filter(
        pago=False, data_vencimento__gte=data_inicio, data_vencimento__lte=data_fim,
    ).exclude(ordem__STATUS='C')

    bruto_receber_por_dia = (
        parcelas_receber.values('data_vencimento').annotate(total=Sum('valor'))
    )
    recebido_por_dia = (
        RecebimentoParcela.objects.filter(
            parcela_ordem__in=parcelas_receber, movimento__status='confirmado',
        )
        .values('parcela_ordem__data_vencimento')
        .annotate(total=Sum('valor_recebido'))
    )

    parcelas_pagar = ParcelaContaPagar.objects.filter(
        pago=False, data_vencimento__gte=data_inicio, data_vencimento__lte=data_fim,
    ).exclude(conta_pagar__status='cancelada')

    bruto_pagar_por_dia = (
        parcelas_pagar.values('data_vencimento').annotate(total=Sum('valor'))
    )
    pago_por_dia = (
        PagamentoParcelaContaPagar.objects.filter(
            parcela_conta_pagar__in=parcelas_pagar, movimento__status='confirmado',
        )
        .values('parcela_conta_pagar__data_vencimento')
        .annotate(total=Sum('valor_pago'))
    )

    buckets = {}

    def acumular(campo_chave, linhas, campo_destino, sinal=1):
        for r in linhas:
            data = r[campo_chave]
            chave = _inicio_periodo(data, agrupamento)
            buckets.setdefault(
                chave, {'a_receber': Decimal('0'), 'a_pagar': Decimal('0')}
            )
            buckets[chave][campo_destino] += sinal * r['total']

    acumular('data_vencimento', bruto_receber_por_dia, 'a_receber', +1)
    acumular('parcela_ordem__data_vencimento', recebido_por_dia, 'a_receber', -1)
    acumular('data_vencimento', bruto_pagar_por_dia, 'a_pagar', +1)
    acumular('parcela_conta_pagar__data_vencimento', pago_por_dia, 'a_pagar', -1)

    resultado = []
    for periodo in sorted(buckets):
        a_receber = buckets[periodo]['a_receber']
        a_pagar = buckets[periodo]['a_pagar']
        resultado.append({
            'periodo': periodo, 'a_receber': a_receber, 'a_pagar': a_pagar,
            'saldo_projetado': a_receber - a_pagar,
        })
    return resultado


# ---------------------------------------------------------------------------
# Contas a receber / a pagar
# ---------------------------------------------------------------------------

def relatorio_contas_receber(data_referencia=None):
    """Retorna totais (não listas) de contas a receber por status: em
    aberto, vencidas, a vencer. 'Pagas' aqui é contagem/soma histórica
    separada, já que uma vez paga a parcela some do saldo em aberto.
    """
    hoje = data_referencia or now().date()

    abertas = ParcelaOrdem.objects.filter(pago=False).exclude(ordem__STATUS='C')
    vencidas = abertas.filter(data_vencimento__lt=hoje)
    a_vencer = abertas.filter(data_vencimento__gte=hoje)
    pagas = ParcelaOrdem.objects.filter(pago=True).exclude(ordem__STATUS='C')

    def saldo_total(qs):
        bruto = qs.aggregate(total=Sum('valor'))['total'] or Decimal('0')
        recebido = RecebimentoParcela.objects.filter(
            parcela_ordem__in=qs, movimento__status='confirmado'
        ).aggregate(total=Sum('valor_recebido'))['total'] or Decimal('0')
        return bruto - recebido

    return {
        'em_aberto': {'quantidade': abertas.count(), 'valor': saldo_total(abertas)},
        'vencidas': {'quantidade': vencidas.count(), 'valor': saldo_total(vencidas)},
        'a_vencer': {'quantidade': a_vencer.count(), 'valor': saldo_total(a_vencer)},
        'pagas': {
            'quantidade': pagas.count(),
            'valor': pagas.aggregate(total=Sum('valor'))['total'] or Decimal('0'),
        },
    }


def relatorio_contas_pagar(data_referencia=None):
    hoje = data_referencia or now().date()

    abertas = ParcelaContaPagar.objects.filter(pago=False).exclude(
        conta_pagar__status='cancelada'
    )
    vencidas = abertas.filter(data_vencimento__lt=hoje)
    a_vencer = abertas.filter(data_vencimento__gte=hoje)
    pagas = ParcelaContaPagar.objects.filter(pago=True).exclude(
        conta_pagar__status='cancelada'
    )

    def saldo_total(qs):
        bruto = qs.aggregate(total=Sum('valor'))['total'] or Decimal('0')
        pago = PagamentoParcelaContaPagar.objects.filter(
            parcela_conta_pagar__in=qs, movimento__status='confirmado'
        ).aggregate(total=Sum('valor_pago'))['total'] or Decimal('0')
        return bruto - pago

    return {
        'em_aberto': {'quantidade': abertas.count(), 'valor': saldo_total(abertas)},
        'vencidas': {'quantidade': vencidas.count(), 'valor': saldo_total(vencidas)},
        'a_vencer': {'quantidade': a_vencer.count(), 'valor': saldo_total(a_vencer)},
        'pagas': {
            'quantidade': pagas.count(),
            'valor': pagas.aggregate(total=Sum('valor'))['total'] or Decimal('0'),
        },
    }


# ---------------------------------------------------------------------------
# Receitas / Despesas por agrupamento
# ---------------------------------------------------------------------------

AGRUPAMENTOS_RECEITA = {
    'categoria': 'categoria__nome',
    'cliente': 'ordem__CLIENTE__NOME',
    'os': 'ordem_id',
    'forma_pagamento': None,  # tratado à parte, ver abaixo
}

AGRUPAMENTOS_DESPESA = {
    'categoria': 'categoria__nome',
    'fornecedor': None,  # via PagamentoParcelaContaPagar -> conta_pagar -> fornecedor
    'centro_custo': 'centro_custo__nome',
}


def relatorio_receitas(data_inicio, data_fim, agrupar_por='categoria'):
    """Receitas (movimentos tipo='entrada') no período, agrupadas por
    categoria, cliente, OS ou forma de pagamento.
    """
    qs = MovimentoFinanceiro.objects.filter(
        tipo='entrada', data__gte=data_inicio, data__lte=data_fim,
    )

    if agrupar_por == 'forma_pagamento':
        dados = (
            qs.filter(recebimentoparcela__isnull=False)
            .values('recebimentoparcela__parcela_ordem__forma_pagamento')
            .annotate(total=Sum('valor'), quantidade=Count('id'))
            .order_by('-total')
        )
        return [
            {
                'chave': d['recebimentoparcela__parcela_ordem__forma_pagamento'],
                'total': d['total'], 'quantidade': d['quantidade'],
            }
            for d in dados
        ]

    campo = AGRUPAMENTOS_RECEITA.get(agrupar_por)
    if campo is None:
        raise ValueError(f'Agrupamento de receita inválido: {agrupar_por}')

    dados = (
        qs.values(campo)
        .annotate(total=Sum('valor'), quantidade=Count('id'))
        .order_by('-total')
    )
    return [{'chave': d[campo], 'total': d['total'], 'quantidade': d['quantidade']} for d in dados]


def relatorio_despesas(data_inicio, data_fim, agrupar_por='categoria'):
    """Despesas (movimentos tipo='saida') no período, agrupadas por
    categoria, fornecedor ou centro de custo.
    """
    qs = MovimentoFinanceiro.objects.filter(
        tipo='saida', data__gte=data_inicio, data__lte=data_fim,
    )

    if agrupar_por == 'fornecedor':
        dados = (
            qs.filter(pagamentoparcelacontapagar__isnull=False)
            .values('pagamentoparcelacontapagar__parcela_conta_pagar__conta_pagar__fornecedor__nome')
            .annotate(total=Sum('valor'), quantidade=Count('id'))
            .order_by('-total')
        )
        chave_campo = 'pagamentoparcelacontapagar__parcela_conta_pagar__conta_pagar__fornecedor__nome'
        return [
            {'chave': d[chave_campo], 'total': d['total'], 'quantidade': d['quantidade']}
            for d in dados
        ]

    campo = AGRUPAMENTOS_DESPESA.get(agrupar_por)
    if campo is None:
        raise ValueError(f'Agrupamento de despesa inválido: {agrupar_por}')

    dados = (
        qs.values(campo)
        .annotate(total=Sum('valor'), quantidade=Count('id'))
        .order_by('-total')
    )
    return [{'chave': d[campo], 'total': d['total'], 'quantidade': d['quantidade']} for d in dados]