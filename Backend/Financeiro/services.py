"""Service Layer do app Financeiro.

Regra do projeto: nenhuma regra financeira complexa em views, templates ou JS.
Toda a lógica de negócio financeira vive aqui.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.db.models import Sum
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from simple_history.utils import bulk_create_with_history

from Core.models import ParcelaOrdem

from .models import (
    ContaFinanceira, ContaPagar, MovimentoFinanceiro, PagamentoParcelaContaPagar,
    ParcelaContaPagar, RecebimentoParcela,
)


class SaldoExcedeError(ValueError):
    """Levantado quando o valor recebido excede o saldo em aberto da parcela."""


class ParcelaJaPagaError(ValueError):
    """Levantado quando se tenta receber uma parcela já totalmente paga."""


def conta_padrao_caixa() -> ContaFinanceira:
    """Retorna (criando se necessário) a conta financeira padrão usada pelos
    fluxos de integração automática vindos do Core (entrada de OS, pagamento
    de parcela via `cadastro_caixa`), enquanto não existir seleção de conta
    na interface (isso é escopo da Fase 8 — Caixa).
    """
    conta, _ = ContaFinanceira.objects.get_or_create(
        nome='Caixa Loja',
        defaults={'tipo': 'caixa'},
    )
    return conta


def saldo_aberto_parcela(parcela: ParcelaOrdem) -> Decimal:
    """Calcula quanto ainda falta receber de uma parcela, considerando todos
    os recebimentos já registrados via Financeiro.
    """
    total_recebido = (
        RecebimentoParcela.objects
        .filter(parcela_ordem=parcela, movimento__status='confirmado')
        .aggregate(total=Sum('valor_recebido'))['total']
        or Decimal('0')
    )
    return parcela.valor - total_recebido


@transaction.atomic
def receber_parcela(parcela_id, valor, conta, usuario, forma_pagamento=None,
                     juros=Decimal('0'), multa=Decimal('0'), desconto=Decimal('0'),
                     data=None, categoria=None):
    """Registra o recebimento (integral ou parcial) de uma parcela de OS.

    - Usa ``select_for_update()`` para impedir que duas requisições concorrentes
      efetivem pagamento da mesma parcela ao mesmo tempo.
    - Rejeita (``SaldoExcedeError``) qualquer valor maior que o saldo em aberto —
      não gera crédito/excedente (decisão de negócio confirmada).
    - Nunca cria ``MovimentoFinanceiro``/``RecebimentoParcela`` se a validação falhar.
    """
    valor = Decimal(str(valor))
    if valor <= 0:
        raise ValueError('O valor recebido deve ser positivo.')

    parcela = ParcelaOrdem.objects.select_for_update().get(pk=parcela_id)

    if parcela.pago:
        raise ParcelaJaPagaError('Esta parcela já está totalmente paga.')

    saldo_aberto = saldo_aberto_parcela(parcela)

    if valor > saldo_aberto:
        raise SaldoExcedeError(
            f'Valor recebido (R$ {valor}) excede o saldo em aberto da parcela '
            f'(R$ {saldo_aberto}). Operação rejeitada.'
        )

    movimento = MovimentoFinanceiro.objects.create(
        conta=conta,
        tipo='entrada',
        valor=valor,
        data=data or now().date(),
        categoria=categoria,
        descricao=f'Parcela {parcela.numero} - OS #{parcela.ordem_id}',
        ordem=parcela.ordem,
        criado_por=usuario,
    )

    recebimento = RecebimentoParcela.objects.create(
        parcela_ordem=parcela,
        movimento=movimento,
        valor_recebido=valor,
        juros=juros,
        multa=multa,
        desconto=desconto,
    )

    novo_saldo_aberto = saldo_aberto - valor
    if novo_saldo_aberto <= Decimal('0'):
        parcela.pago = True
        parcela.data_pagamento = data or now().date()
        if forma_pagamento:
            parcela.forma_pagamento = forma_pagamento
        parcela.save(update_fields=['pago', 'data_pagamento', 'forma_pagamento'])

    return movimento, recebimento


# ---------------------------------------------------------------------------
# Contas a pagar (Fase 7)
# ---------------------------------------------------------------------------

class SaldoExcedePagarError(ValueError):
    """Levantado quando o valor pago excede o saldo em aberto da parcela de
    conta a pagar."""


class ParcelaJaPagaPagarError(ValueError):
    """Levantado quando se tenta pagar uma parcela de conta a pagar já
    totalmente quitada."""


@transaction.atomic
def criar_conta_pagar(descricao, valor_total, data_emissao, quantidade_parcelas=1,
                       fornecedor=None, categoria=None, centro_custo=None,
                       recorrente=False, primeiro_vencimento=None):
    """Cria uma ContaPagar e suas parcelas, com o mesmo cuidado de
    arredondamento de `Core.utils.criar_parcelas`: o resíduo de centavos vai
    inteiro para a última parcela, garantindo soma exata.
    """
    valor_total = Decimal(str(valor_total))
    if valor_total <= 0:
        raise ValueError('O valor total deve ser positivo.')
    if quantidade_parcelas <= 0:
        raise ValueError('A quantidade de parcelas deve ser positiva.')

    conta = ContaPagar.objects.create(
        fornecedor=fornecedor,
        descricao=descricao,
        categoria=categoria,
        centro_custo=centro_custo,
        valor_total=valor_total,
        data_emissao=data_emissao,
        recorrente=recorrente,
    )

    valor_parcela = (valor_total / quantidade_parcelas).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP
    )
    base_vencimento = primeiro_vencimento or data_emissao

    parcelas = []
    soma = Decimal('0')
    for i in range(1, quantidade_parcelas + 1):
        vencimento = base_vencimento + relativedelta(months=i - 1)
        if i == quantidade_parcelas:
            valor_esta = valor_total - soma
        else:
            valor_esta = valor_parcela
            soma += valor_parcela
        parcelas.append(ParcelaContaPagar(
            conta_pagar=conta, numero=i, data_vencimento=vencimento, valor=valor_esta,
        ))

    bulk_create_with_history(parcelas, ParcelaContaPagar, batch_size=500)
    return conta


def saldo_aberto_parcela_pagar(parcela: ParcelaContaPagar) -> Decimal:
    total_pago = (
        PagamentoParcelaContaPagar.objects
        .filter(parcela_conta_pagar=parcela, movimento__status='confirmado')
        .aggregate(total=Sum('valor_pago'))['total']
        or Decimal('0')
    )
    return parcela.valor - total_pago


@transaction.atomic
def pagar_parcela_conta_pagar(parcela_id, valor, conta, usuario,
                               juros=Decimal('0'), multa=Decimal('0'),
                               desconto=Decimal('0'), data=None, categoria=None,
                               centro_custo=None):
    """Registra o pagamento (integral ou parcial) de uma parcela de conta a
    pagar. Mesmas garantias do lado de contas a receber: lock por
    `select_for_update`, rejeição de excedente, nunca cria registro se a
    validação falhar.
    """
    valor = Decimal(str(valor))
    if valor <= 0:
        raise ValueError('O valor pago deve ser positivo.')

    parcela = ParcelaContaPagar.objects.select_for_update().get(pk=parcela_id)

    if parcela.pago:
        raise ParcelaJaPagaPagarError('Esta parcela já está totalmente paga.')

    saldo_aberto = saldo_aberto_parcela_pagar(parcela)

    if valor > saldo_aberto:
        raise SaldoExcedePagarError(
            f'Valor pago (R$ {valor}) excede o saldo em aberto da parcela '
            f'(R$ {saldo_aberto}). Operação rejeitada.'
        )

    movimento = MovimentoFinanceiro.objects.create(
        conta=conta,
        tipo='saida',
        valor=valor,
        data=data or now().date(),
        categoria=categoria or parcela.conta_pagar.categoria,
        centro_custo=centro_custo or parcela.conta_pagar.centro_custo,
        descricao=f'Parcela {parcela.numero} - {parcela.conta_pagar.descricao}',
        criado_por=usuario,
    )

    pagamento = PagamentoParcelaContaPagar.objects.create(
        parcela_conta_pagar=parcela,
        movimento=movimento,
        valor_pago=valor,
        juros=juros,
        multa=multa,
        desconto=desconto,
    )

    novo_saldo_aberto = saldo_aberto - valor
    if novo_saldo_aberto <= Decimal('0'):
        parcela.pago = True
        parcela.data_pagamento = data or now().date()
        parcela.save(update_fields=['pago', 'data_pagamento'])

    _atualizar_status_conta_pagar(parcela.conta_pagar)

    return movimento, pagamento


def _atualizar_status_conta_pagar(conta_pagar: ContaPagar):
    parcelas = conta_pagar.parcelas.all()
    if not parcelas.exists():
        return
    if all(p.pago for p in parcelas):
        novo_status = 'paga'
    elif any(p.pago for p in parcelas) or any(
        saldo_aberto_parcela_pagar(p) < p.valor for p in parcelas
    ):
        novo_status = 'parcial'
    else:
        novo_status = 'pendente'

    if conta_pagar.status != novo_status and conta_pagar.status != 'cancelada':
        conta_pagar.status = novo_status
        conta_pagar.save(update_fields=['status'])


# ---------------------------------------------------------------------------
# Caixa: abertura, sangria, suprimento, fechamento (Fase 8)
# ---------------------------------------------------------------------------
from django.db import IntegrityError  # noqa: E402

from .models import FechamentoCaixa  # noqa: E402


class CaixaJaAbertoError(ValueError):
    """Levantado ao tentar abrir um caixa em uma conta que já tem um
    fechamento em aberto."""


class CaixaJaFechadoError(ValueError):
    """Levantado ao tentar operar sobre um fechamento de caixa que já foi
    encerrado."""


class MotivoDiferencaObrigatorioError(ValueError):
    """Levantado ao tentar fechar um caixa com diferença sem informar o
    motivo (regra 52 do prompt original: ação crítica exige motivo)."""


def saldo_atual_conta(conta: ContaFinanceira, ate_data=None) -> Decimal:
    """Saldo derivado: saldo_inicial + entradas/suprimentos - saídas/sangrias.

    Importante: NÃO filtra por `status='confirmado'`. Um movimento estornado
    e seu estorno são dois lançamentos de sinal oposto que já se cancelam
    matematicamente quando ambos são somados (partida dobrada). Excluir o
    original por status e somar só o estorno causaria dupla contagem do
    efeito da reversão. O campo `status` serve para auditoria/exibição
    ("este lançamento foi estornado"), não para filtrar o cálculo de saldo.

    `transferencia`, `estorno` e `ajuste` ainda não têm semântica de sinal
    definida e são propositalmente excluídos aqui — ver
    docs/financeiro/06-casos-extremos.md.
    """
    qs = MovimentoFinanceiro.objects.filter(conta=conta)
    if ate_data:
        qs = qs.filter(data__lte=ate_data)

    entradas = qs.filter(tipo__in=MovimentoFinanceiro.TIPOS_ENTRADA).aggregate(
        total=Sum('valor'))['total'] or Decimal('0')
    saidas = qs.filter(tipo__in=MovimentoFinanceiro.TIPOS_SAIDA).aggregate(
        total=Sum('valor'))['total'] or Decimal('0')

    return conta.saldo_inicial + entradas - saidas


@transaction.atomic
def abrir_caixa_financeiro(conta, usuario, saldo_abertura=None, data=None):
    if FechamentoCaixa.objects.filter(conta=conta, status='aberto').exists():
        raise CaixaJaAbertoError(
            f'Já existe um caixa aberto para a conta "{conta}". Feche-o antes de abrir outro.'
        )

    if saldo_abertura is None:
        saldo_abertura = saldo_atual_conta(conta)

    try:
        return FechamentoCaixa.objects.create(
            conta=conta,
            data=data or now().date(),
            saldo_abertura=Decimal(str(saldo_abertura)),
            aberto_por=usuario,
        )
    except IntegrityError:
        # corrida entre duas aberturas simultâneas - a constraint do banco
        # pega o que a checagem acima (não atômica sozinha) pode deixar passar
        raise CaixaJaAbertoError(
            f'Já existe um caixa aberto para a conta "{conta}".'
        )


def _registrar_movimento_caixa(conta, tipo, valor, usuario, descricao='',
                                data=None, categoria=None, centro_custo=None):
    valor = Decimal(str(valor))
    if valor <= 0:
        raise ValueError('O valor do movimento deve ser positivo.')
    return MovimentoFinanceiro.objects.create(
        conta=conta,
        tipo=tipo,
        valor=valor,
        data=data or now().date(),
        categoria=categoria,
        centro_custo=centro_custo,
        descricao=descricao,
        criado_por=usuario,
    )


def registrar_sangria(conta, valor, usuario, motivo, data=None):
    """Retirada de dinheiro do caixa. Nunca classificada automaticamente
    como despesa operacional — é seu próprio tipo (regra 22 do prompt
    original)."""
    if not motivo:
        raise ValueError('Sangria exige motivo.')
    return _registrar_movimento_caixa(
        conta, 'sangria', valor, usuario, descricao=f'Sangria: {motivo}', data=data,
    )


def registrar_suprimento(conta, valor, usuario, descricao='', data=None):
    """Reforço de caixa. Nunca classificado automaticamente como receita
    operacional (regra 23 do prompt original)."""
    return _registrar_movimento_caixa(
        conta, 'suprimento', valor, usuario,
        descricao=descricao or 'Suprimento de caixa', data=data,
    )


@transaction.atomic
def fechar_caixa_financeiro(fechamento_id, saldo_contado, usuario, motivo_diferenca=''):
    fechamento = FechamentoCaixa.objects.select_for_update().get(pk=fechamento_id)

    if fechamento.status == 'fechado':
        raise CaixaJaFechadoError('Este caixa já foi fechado.')

    saldo_contado = Decimal(str(saldo_contado))
    saldo_esperado = saldo_atual_conta(fechamento.conta)
    diferenca = saldo_contado - saldo_esperado

    if diferenca != Decimal('0') and not motivo_diferenca:
        raise MotivoDiferencaObrigatorioError(
            f'Há uma diferença de R$ {diferenca} entre o saldo esperado '
            f'(R$ {saldo_esperado}) e o contado (R$ {saldo_contado}). '
            'Informe o motivo para poder fechar o caixa.'
        )

    fechamento.saldo_esperado = saldo_esperado
    fechamento.saldo_contado = saldo_contado
    fechamento.diferenca = diferenca
    fechamento.motivo_diferenca = motivo_diferenca
    fechamento.status = 'fechado'
    fechamento.fechado_por = usuario
    fechamento.fechado_em = now()
    fechamento._change_reason = (
        motivo_diferenca if diferenca != Decimal('0') else 'Fechamento sem diferença'
    )
    fechamento.save(update_fields=[
        'saldo_esperado', 'saldo_contado', 'diferenca', 'motivo_diferenca',
        'status', 'fechado_por', 'fechado_em',
    ])
    return fechamento


# ---------------------------------------------------------------------------
# Estornos (Fase 9)
# ---------------------------------------------------------------------------
from .models import EstornoFinanceiro  # noqa: E402

# Mapa de tipo oposto usado para gerar o movimento inverso. `transferencia`,
# `estorno` e `ajuste` ainda não têm oposto definido (dependem de desenhos
# futuros: transferência precisa dos dois lados, estorno de estorno não faz
# sentido, ajuste é caso a caso) — estornar um movimento desses tipos
# levanta erro explícito em vez de assumir um comportamento.
TIPO_OPOSTO = {
    'entrada': 'saida',
    'saida': 'entrada',
    'sangria': 'suprimento',
    'suprimento': 'sangria',
}


class MovimentoJaEstornadoError(ValueError):
    """Levantado ao tentar estornar um movimento que já foi estornado."""


class TipoNaoEstornavelError(ValueError):
    """Levantado ao tentar estornar um movimento cujo tipo ainda não tem
    oposto definido (transferência, estorno, ajuste)."""


@transaction.atomic
def estornar_movimento(movimento_id, usuario, motivo):
    """Estorna um movimento financeiro: nunca apaga o original, cria o
    inverso e liga os dois via `EstornoFinanceiro` (regra 30 do prompt
    original). Se o movimento estornado alimentava um `RecebimentoParcela`
    ou `PagamentoParcelaContaPagar` que havia quitado a parcela, a parcela
    volta para "em aberto" automaticamente.
    """
    if not motivo:
        raise ValueError('Estorno exige motivo.')

    movimento = MovimentoFinanceiro.objects.select_for_update().get(pk=movimento_id)

    if movimento.status == 'estornado':
        raise MovimentoJaEstornadoError('Este movimento já foi estornado.')

    if hasattr(movimento, 'estorno'):
        # defesa extra além da OneToOneField — não deveria acontecer se
        # status já estiver consistente, mas nunca confie só em um dos dois
        raise MovimentoJaEstornadoError('Este movimento já foi estornado.')

    tipo_oposto = TIPO_OPOSTO.get(movimento.tipo)
    if tipo_oposto is None:
        raise TipoNaoEstornavelError(
            f'Movimentos do tipo "{movimento.tipo}" ainda não têm estorno automático suportado.'
        )

    movimento_estorno = MovimentoFinanceiro.objects.create(
        conta=movimento.conta,
        tipo=tipo_oposto,
        valor=movimento.valor,
        data=now().date(),
        categoria=movimento.categoria,
        centro_custo=movimento.centro_custo,
        descricao=f'Estorno do movimento #{movimento.id}: {motivo}',
        ordem=movimento.ordem,
        criado_por=usuario,
    )

    movimento.status = 'estornado'
    movimento._change_reason = motivo
    movimento.save(update_fields=['status'])

    estorno = EstornoFinanceiro.objects.create(
        movimento_original=movimento,
        movimento_estorno=movimento_estorno,
        usuario=usuario,
        motivo=motivo,
    )

    # Se esse movimento tinha quitado uma parcela (receber ou pagar), a
    # parcela volta a ficar em aberto — recalculado a partir do saldo real,
    # já que saldo_aberto_parcela/saldo_aberto_parcela_pagar filtram por
    # movimento__status='confirmado' e este movimento acabou de sair dessa
    # condição.
    recebimento = RecebimentoParcela.objects.filter(movimento=movimento).first()
    if recebimento and recebimento.parcela_ordem.pago:
        parcela = recebimento.parcela_ordem
        if saldo_aberto_parcela(parcela) > Decimal('0'):
            parcela.pago = False
            parcela.save(update_fields=['pago'])

    pagamento = PagamentoParcelaContaPagar.objects.filter(movimento=movimento).first()
    if pagamento and pagamento.parcela_conta_pagar.pago:
        parcela_pagar = pagamento.parcela_conta_pagar
        if saldo_aberto_parcela_pagar(parcela_pagar) > Decimal('0'):
            parcela_pagar.pago = False
            parcela_pagar.save(update_fields=['pago'])
        _atualizar_status_conta_pagar(parcela_pagar.conta_pagar)

    return estorno


def usuario_sistema():
    """Usuário técnico usado para ações automáticas (ex: estorno automático
    disparado por signal, sem requisição HTTP associada). Criado sob demanda.
    """
    from django.contrib.auth import get_user_model
    Usuario = get_user_model()
    usuario, _ = Usuario.objects.get_or_create(
        username='sistema_financeiro',
        defaults={'first_name': 'Sistema Financeiro', 'is_active': False},
    )
    return usuario


def usuario_para_estorno_automatico():
    """Tenta recuperar o usuário da requisição HTTP em andamento (via o
    thread-local do `simple_history.middleware.HistoryRequestMiddleware`,
    já habilitado no projeto). Se não houver requisição associada (ex:
    signal disparado em um teste, comando de management, ou script), usa o
    usuário técnico `usuario_sistema()`.
    """
    try:
        from simple_history.models import HistoricalRecords
        request = getattr(HistoricalRecords.context, 'request', None)
        user = getattr(request, 'user', None)
        if user is not None and getattr(user, 'is_authenticated', False):
            return user
    except Exception:
        pass
    return usuario_sistema()


# ---------------------------------------------------------------------------
# Dashboard (Fase 11)
# ---------------------------------------------------------------------------
from datetime import timedelta  # noqa: E402


def _total_a_receber_queryset(qs_parcelas):
    """Dado um queryset de `ParcelaOrdem` não pagas, calcula o total em
    aberto (valor da parcela menos o que já foi recebido parcialmente),
    usando duas agregações no banco em vez de iterar linha a linha em
    Python (evita N+1)."""
    total_valor = qs_parcelas.aggregate(total=Sum('valor'))['total'] or Decimal('0')
    total_recebido = RecebimentoParcela.objects.filter(
        parcela_ordem__in=qs_parcelas, movimento__status='confirmado'
    ).aggregate(total=Sum('valor_recebido'))['total'] or Decimal('0')
    return total_valor - total_recebido


def _total_a_pagar_queryset(qs_parcelas):
    total_valor = qs_parcelas.aggregate(total=Sum('valor'))['total'] or Decimal('0')
    total_pago = PagamentoParcelaContaPagar.objects.filter(
        parcela_conta_pagar__in=qs_parcelas, movimento__status='confirmado'
    ).aggregate(total=Sum('valor_pago'))['total'] or Decimal('0')
    return total_valor - total_pago


def dashboard_financeiro(data_referencia=None):
    """Monta os indicadores da seção 36 do prompt original. Todas as somas
    usam `aggregate()` no banco — nenhum loop Python sobre parcelas
    individuais para calcular totais (evita N+1 mesmo com muitos registros).

    Convenção adotada aqui: "entradas"/"saídas" de caixa incluem
    suprimento/sangria (são dinheiro entrando/saindo fisicamente da conta),
    mesma convenção de `saldo_atual_conta()`. Quem quiser separar "receita
    operacional" de "reforço de caixa" deve usar os relatórios por tipo
    (Fase 12), não este indicador agregado.
    """
    hoje = data_referencia or now().date()
    inicio_mes = hoje.replace(day=1)

    # --- saldo por conta e saldo total ---
    contas = list(ContaFinanceira.objects.filter(ativa=True))
    saldo_por_conta = {c.id: saldo_atual_conta(c) for c in contas}
    saldo_total = sum(saldo_por_conta.values(), Decimal('0'))

    # --- movimentação do dia e do mês (uma agregação cada, não por conta) ---
    def entradas_saidas(data_inicio, data_fim):
        qs = MovimentoFinanceiro.objects.filter(data__gte=data_inicio, data__lte=data_fim)
        entradas = qs.filter(tipo__in=MovimentoFinanceiro.TIPOS_ENTRADA).aggregate(
            total=Sum('valor'))['total'] or Decimal('0')
        saidas = qs.filter(tipo__in=MovimentoFinanceiro.TIPOS_SAIDA).aggregate(
            total=Sum('valor'))['total'] or Decimal('0')
        return entradas, saidas

    entradas_hoje, saidas_hoje = entradas_saidas(hoje, hoje)
    entradas_mes, saidas_mes = entradas_saidas(inicio_mes, hoje)

    # --- contas a receber (Core.ParcelaOrdem, excluindo OS canceladas) ---
    parcelas_receber_abertas = ParcelaOrdem.objects.filter(pago=False).exclude(
        ordem__STATUS='C'
    )
    total_a_receber = _total_a_receber_queryset(parcelas_receber_abertas)
    total_vencido_receber = _total_a_receber_queryset(
        parcelas_receber_abertas.filter(data_vencimento__lt=hoje)
    )

    # --- contas a pagar ---
    parcelas_pagar_abertas = ParcelaContaPagar.objects.filter(pago=False).exclude(
        conta_pagar__status='cancelada'
    )
    total_a_pagar = _total_a_pagar_queryset(parcelas_pagar_abertas)
    total_vencido_pagar = _total_a_pagar_queryset(
        parcelas_pagar_abertas.filter(data_vencimento__lt=hoje)
    )

    # --- próximos vencimentos (próximos 7 dias), com select_related para
    #     evitar N+1 ao exibir cliente/fornecedor na lista ---
    limite = hoje + timedelta(days=7)
    recebimentos_proximos = list(
        parcelas_receber_abertas
        .filter(data_vencimento__gte=hoje, data_vencimento__lte=limite)
        .select_related('ordem', 'ordem__CLIENTE')
        .order_by('data_vencimento')[:20]
    )
    pagamentos_proximos = list(
        parcelas_pagar_abertas
        .filter(data_vencimento__gte=hoje, data_vencimento__lte=limite)
        .select_related('conta_pagar', 'conta_pagar__fornecedor')
        .order_by('data_vencimento')[:20]
    )

    return {
        'data_referencia': hoje,
        'saldo_total': saldo_total,
        'saldo_por_conta': saldo_por_conta,
        'entradas_hoje': entradas_hoje,
        'saidas_hoje': saidas_hoje,
        'entradas_mes': entradas_mes,
        'saidas_mes': saidas_mes,
        'resultado_mes': entradas_mes - saidas_mes,
        'total_a_receber': total_a_receber,
        'total_a_pagar': total_a_pagar,
        'total_vencido_receber': total_vencido_receber,
        'total_vencido_pagar': total_vencido_pagar,
        'total_vencido': total_vencido_receber + total_vencido_pagar,
        'recebimentos_proximos': recebimentos_proximos,
        'pagamentos_proximos': pagamentos_proximos,
    }