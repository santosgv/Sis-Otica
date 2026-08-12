from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from Core.models import ParcelaOrdem

from .models import ContaFinanceira, ContaPagar, FechamentoCaixa, ParcelaContaPagar
from .services import (
    CaixaJaAbertoError,
    CaixaJaFechadoError,
    MotivoDiferencaObrigatorioError,
    ParcelaJaPagaError,
    ParcelaJaPagaPagarError,
    SaldoExcedeError,
    SaldoExcedePagarError,
    abrir_caixa_financeiro,
    conta_padrao_caixa,
    criar_conta_pagar,
    dashboard_financeiro,
    fechar_caixa_financeiro,
    pagar_parcela_conta_pagar,
    receber_parcela,
    registrar_sangria,
    registrar_suprimento,
    saldo_atual_conta,
)
from .relatorios import relatorio_contas_pagar, relatorio_contas_receber


def _parse_valor(valor_str):
    """Aceita tanto '1234.56' quanto '1.234,56' (formato brasileiro)."""
    if not valor_str:
        raise ValueError('Valor não informado.')
    limpo = valor_str.strip()
    if ',' in limpo:
        limpo = limpo.replace('.', '').replace(',', '.')
    try:
        return Decimal(limpo)
    except InvalidOperation:
        raise ValueError(f'Valor inválido: {valor_str}')


@login_required(login_url='/auth/logar/')
def dashboard(request):
    dados = dashboard_financeiro()
    return render(request, 'Financeiro/dashboard.html', {'dados': dados})


@login_required(login_url='/auth/logar/')
def contas_a_receber(request):
    parcelas = (
        ParcelaOrdem.objects.filter(pago=False)
        .exclude(ordem__STATUS='C')
        .select_related('ordem', 'ordem__CLIENTE')
        .order_by('data_vencimento')
    )
    resumo = relatorio_contas_receber()
    return render(request, 'Financeiro/contas_a_receber.html', {
        'parcelas': parcelas, 'resumo': resumo, 'hoje': now().date(),
    })


@login_required(login_url='/auth/logar/')
def receber_parcela_view(request, parcela_id):
    if request.method != 'POST':
        return redirect('Financeiro:contas_a_receber')

    parcela = get_object_or_404(ParcelaOrdem, pk=parcela_id)

    try:
        valor = _parse_valor(request.POST.get('VALOR'))
        conta = conta_padrao_caixa()
        receber_parcela(
            parcela.id, valor, conta, request.user,
            forma_pagamento=request.POST.get('FORMA') or None,
        )
        messages.add_message(
            request, django_messages.SUCCESS,
            f'Recebimento de R$ {valor} registrado para a parcela {parcela.numero} '
            f'(OS #{parcela.ordem_id}).'
        )
    except (SaldoExcedeError, ParcelaJaPagaError, ValueError) as e:
        messages.add_message(request, django_messages.ERROR, str(e))

    return redirect('Financeiro:contas_a_receber')


@login_required(login_url='/auth/logar/')
def contas_a_pagar(request):
    contas = ContaPagar.objects.exclude(status='cancelada').select_related(
        'fornecedor'
    ).prefetch_related('parcelas').order_by('-data_emissao')
    resumo = relatorio_contas_pagar()
    return render(request, 'Financeiro/contas_a_pagar.html', {
        'contas': contas, 'resumo': resumo, 'hoje': now().date(),
    })


@login_required(login_url='/auth/logar/')
def nova_conta_pagar(request):
    if request.method == 'POST':
        try:
            descricao = request.POST.get('DESCRICAO')
            if not descricao:
                raise ValueError('Descrição é obrigatória.')
            valor_total = _parse_valor(request.POST.get('VALOR_TOTAL'))
            quantidade_parcelas = int(request.POST.get('QUANTIDADE_PARCELAS') or 1)

            criar_conta_pagar(
                descricao, valor_total, now().date(),
                quantidade_parcelas=quantidade_parcelas,
            )
            messages.add_message(
                request, django_messages.SUCCESS, 'Conta a pagar criada com sucesso.'
            )
            return redirect('Financeiro:contas_a_pagar')
        except ValueError as e:
            messages.add_message(request, django_messages.ERROR, str(e))

    return render(request, 'Financeiro/nova_conta_pagar.html')


@login_required(login_url='/auth/logar/')
def pagar_parcela_view(request, parcela_id):
    if request.method != 'POST':
        return redirect('Financeiro:contas_a_pagar')

    parcela = get_object_or_404(ParcelaContaPagar, pk=parcela_id)

    try:
        valor = _parse_valor(request.POST.get('VALOR'))
        conta = conta_padrao_caixa()
        pagar_parcela_conta_pagar(parcela.id, valor, conta, request.user)
        messages.add_message(
            request, django_messages.SUCCESS,
            f'Pagamento de R$ {valor} registrado para a parcela {parcela.numero} '
            f'de "{parcela.conta_pagar.descricao}".'
        )
    except (SaldoExcedePagarError, ParcelaJaPagaPagarError, ValueError) as e:
        messages.add_message(request, django_messages.ERROR, str(e))

    return redirect('Financeiro:contas_a_pagar')


@login_required(login_url='/auth/logar/')
def caixa(request):
    contas = ContaFinanceira.objects.filter(ativa=True)
    linhas = []
    for c in contas:
        fechamento_aberto = FechamentoCaixa.objects.filter(
            conta=c, status='aberto'
        ).first()
        linhas.append({
            'conta': c,
            'saldo_atual': saldo_atual_conta(c),
            'fechamento_aberto': fechamento_aberto,
        })

    movimentos_recentes = (
        contas.first().movimentos.select_related('categoria', 'ordem').order_by(
            '-data', '-id'
        )[:20] if contas.exists() else []
    )

    return render(request, 'Financeiro/caixa.html', {
        'linhas': linhas, 'movimentos_recentes': movimentos_recentes,
    })


@login_required(login_url='/auth/logar/')
def abrir_caixa_view(request):
    if request.method == 'POST':
        conta = get_object_or_404(ContaFinanceira, pk=request.POST.get('CONTA_ID'))
        try:
            abrir_caixa_financeiro(conta, request.user)
            messages.add_message(
                request, django_messages.SUCCESS, f'Caixa aberto para "{conta}".'
            )
        except CaixaJaAbertoError as e:
            messages.add_message(request, django_messages.ERROR, str(e))
    return redirect('Financeiro:caixa')


@login_required(login_url='/auth/logar/')
def fechar_caixa_view(request, fechamento_id):
    if request.method == 'POST':
        try:
            saldo_contado = _parse_valor(request.POST.get('SALDO_CONTADO'))
            motivo = request.POST.get('MOTIVO_DIFERENCA', '')
            fechar_caixa_financeiro(fechamento_id, saldo_contado, request.user, motivo)
            messages.add_message(
                request, django_messages.SUCCESS, 'Caixa fechado com sucesso.'
            )
        except (CaixaJaFechadoError, MotivoDiferencaObrigatorioError, ValueError) as e:
            messages.add_message(request, django_messages.ERROR, str(e))
    return redirect('Financeiro:caixa')


@login_required(login_url='/auth/logar/')
def sangria_view(request):
    if request.method == 'POST':
        try:
            conta = get_object_or_404(ContaFinanceira, pk=request.POST.get('CONTA_ID'))
            valor = _parse_valor(request.POST.get('VALOR'))
            motivo = request.POST.get('MOTIVO', '')
            registrar_sangria(conta, valor, request.user, motivo)
            messages.add_message(
                request, django_messages.SUCCESS, f'Sangria de R$ {valor} registrada.'
            )
        except ValueError as e:
            messages.add_message(request, django_messages.ERROR, str(e))
    return redirect('Financeiro:caixa')


@login_required(login_url='/auth/logar/')
def suprimento_view(request):
    if request.method == 'POST':
        try:
            conta = get_object_or_404(ContaFinanceira, pk=request.POST.get('CONTA_ID'))
            valor = _parse_valor(request.POST.get('VALOR'))
            descricao = request.POST.get('DESCRICAO', '')
            registrar_suprimento(conta, valor, request.user, descricao)
            messages.add_message(
                request, django_messages.SUCCESS, f'Suprimento de R$ {valor} registrado.'
            )
        except ValueError as e:
            messages.add_message(request, django_messages.ERROR, str(e))
    return redirect('Financeiro:caixa')