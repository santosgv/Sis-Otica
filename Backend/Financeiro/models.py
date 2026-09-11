from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from simple_history.models import HistoricalRecords


class ContaFinanceira(models.Model):
    """Conta financeira real (caixa físico, banco, PIX, etc).

    O saldo atual nunca é armazenado diretamente: é sempre derivado de
    ``saldo_inicial`` + agregação dos ``MovimentoFinanceiro`` dessa conta.
    Isso evita inconsistência de saldo sem histórico (ver docs/financeiro/04-modelagem.md).
    """

    TIPO_CHOICES = [
        ('caixa', 'Caixa'),
        ('banco', 'Banco'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    banco = models.CharField(max_length=100, blank=True)
    agencia = models.CharField(max_length=20, blank=True)
    numero_conta = models.CharField(max_length=30, blank=True)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Conta Financeira'
        verbose_name_plural = 'Contas Financeiras'
        ordering = ['nome']

    def __str__(self) -> str:
        return str(self.nome)


class CategoriaFinanceira(models.Model):
    """Categoria hierárquica de receita ou despesa.

    Nunca é excluída fisicamente se estiver em uso — ``categoria_pai`` usa
    ``PROTECT`` para impedir exclusão de categoria com filhas, e o padrão
    esperado para "desativar" uma categoria em uso é marcar ``ativa=False``,
    nunca fazer ``.delete()``.
    """

    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria_pai = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='filhas',
    )
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoria Financeira'
        verbose_name_plural = 'Categorias Financeiras'
        ordering = ['tipo', 'nome']

    def __str__(self) -> str:
        return str(self.nome)

    def clean(self):
        # Categoria pai deve ser do mesmo tipo (receita não pode ser filha de despesa)
        if self.categoria_pai_id and self.categoria_pai.tipo != self.tipo:
            raise ValidationError(
                'A categoria pai deve ser do mesmo tipo (receita/despesa).'
            )


class CentroCusto(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'
        ordering = ['nome']

    def __str__(self) -> str:
        return str(self.nome)


class MovimentoFinanceiro(models.Model):
    """Lançamento financeiro individual (entrada, saída, transferência,
    estorno, ajuste, sangria ou suprimento).

    ``valor`` é sempre armazenado positivo. O sinal (soma ou subtrai do saldo
    da conta) é determinado pelo ``tipo`` no momento de agregar o saldo,
    nunca pelo sinal do próprio campo.
    """

    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('transferencia', 'Transferência'),
        ('estorno', 'Estorno'),
        ('ajuste', 'Ajuste'),
        ('sangria', 'Sangria'),
        ('suprimento', 'Suprimento'),
    ]

    # tipos que somam no saldo da conta
    TIPOS_ENTRADA = {'entrada', 'suprimento'}
    # tipos que subtraem do saldo da conta
    TIPOS_SAIDA = {'saida', 'sangria'}

    STATUS_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('estornado', 'Estornado'),
    ]

    conta = models.ForeignKey(
        ContaFinanceira, on_delete=models.PROTECT, related_name='movimentos'
    )
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(
        CategoriaFinanceira, null=True, blank=True, on_delete=models.PROTECT
    )
    centro_custo = models.ForeignKey(
        CentroCusto, null=True, blank=True, on_delete=models.PROTECT
    )
    descricao = models.CharField(max_length=255, blank=True)

    # rastreio da origem comercial — aponta para o Core, nunca o contrário
    ordem = models.ForeignKey(
        'Core.ORDEN', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='movimentos_financeiros',
    )

    transferencia_par = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='par_oposto',
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='confirmado')

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Movimento Financeiro'
        verbose_name_plural = 'Movimentos Financeiros'
        ordering = ['-data', '-id']
        indexes = [
            models.Index(fields=['conta', 'data']),
            models.Index(fields=['ordem']),
        ]

    def __str__(self) -> str:
        return f'{self.get_tipo_display()} R$ {self.valor} - {self.conta}'

    def clean(self):
        if self.valor is not None and self.valor <= 0:
            raise ValidationError('O valor do movimento deve ser positivo.')


class RecebimentoParcela(models.Model):
    """Liga uma ``Core.ParcelaOrdem`` a um ``MovimentoFinanceiro``.

    Uma parcela pode ter vários recebimentos ao longo do tempo (pagamento
    parcial) até que a soma de ``valor_recebido`` atinja o valor da parcela.
    O sistema rejeita qualquer recebimento que exceda o saldo em aberto da
    parcela (decisão de negócio confirmada — ver docs/financeiro/06-casos-extremos.md).
    """

    parcela_ordem = models.ForeignKey(
        'Core.ParcelaOrdem', on_delete=models.PROTECT,
        related_name='recebimentos_financeiro',
    )
    movimento = models.OneToOneField(MovimentoFinanceiro, on_delete=models.PROTECT)
    valor_recebido = models.DecimalField(max_digits=12, decimal_places=2)
    juros = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    multa = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recebimento de Parcela'
        verbose_name_plural = 'Recebimentos de Parcela'
        ordering = ['-criado_em']

    def __str__(self) -> str:
        return f'Recebimento R$ {self.valor_recebido} - Parcela {self.parcela_ordem_id}'


class ContaPagar(models.Model):
    """Obrigação financeira de despesa (fornecedor ou despesa manual),
    equivalente a uma "Ordem" do lado de contas a pagar. Não se apaga
    fisicamente — cancelamento é um status, nunca um delete.
    """

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('parcial', 'Parcialmente paga'),
        ('paga', 'Paga'),
        ('cancelada', 'Cancelada'),
    ]

    fornecedor = models.ForeignKey(
        'Core.Fornecedor', null=True, blank=True, on_delete=models.PROTECT
    )
    descricao = models.CharField(max_length=255)
    categoria = models.ForeignKey(
        CategoriaFinanceira, null=True, blank=True, on_delete=models.PROTECT
    )
    centro_custo = models.ForeignKey(
        CentroCusto, null=True, blank=True, on_delete=models.PROTECT
    )
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    data_emissao = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    # base para seção 47 do prompt original (recorrências) — sem lógica extra por ora
    recorrente = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['-data_emissao']

    def __str__(self) -> str:
        return f'{self.descricao} - R$ {self.valor_total}'

    def clean(self):
        if self.valor_total is not None and self.valor_total <= 0:
            raise ValidationError('O valor total deve ser positivo.')


class ParcelaContaPagar(models.Model):
    conta_pagar = models.ForeignKey(
        ContaPagar, on_delete=models.CASCADE, related_name='parcelas'
    )
    numero = models.IntegerField()
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Parcela de Conta a Pagar'
        verbose_name_plural = 'Parcelas de Conta a Pagar'
        ordering = ['conta_pagar', 'numero']
        constraints = [
            models.UniqueConstraint(
                fields=['conta_pagar', 'numero'], name='parcela_unica_por_conta_pagar'
            )
        ]

    def __str__(self) -> str:
        return f'Parcela {self.numero} - {self.conta_pagar}'


class PagamentoParcelaContaPagar(models.Model):
    """Liga uma ``ParcelaContaPagar`` a um ``MovimentoFinanceiro`` de saída.

    Espelha ``RecebimentoParcela``: uma parcela de conta a pagar pode ter
    vários pagamentos parciais até `sum(valor_pago) == parcela.valor`. Valor
    que excede o saldo em aberto é rejeitado (mesma regra de negócio das
    contas a receber).
    """

    parcela_conta_pagar = models.ForeignKey(
        ParcelaContaPagar, on_delete=models.PROTECT, related_name='pagamentos'
    )
    movimento = models.OneToOneField(MovimentoFinanceiro, on_delete=models.PROTECT)
    valor_pago = models.DecimalField(max_digits=12, decimal_places=2)
    juros = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    multa = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pagamento de Parcela (Conta a Pagar)'
        verbose_name_plural = 'Pagamentos de Parcela (Conta a Pagar)'
        ordering = ['-criado_em']

    def __str__(self) -> str:
        return f'Pagamento R$ {self.valor_pago} - {self.parcela_conta_pagar}'


class FechamentoCaixa(models.Model):
    """Um registro por abertura/fechamento de caixa em uma conta.

    Diferente de `Core.CAIXA` (que usa flags soltas `ABERTO`/`FECHADO` em
    cada lançamento), aqui existe UM registro por período de caixa aberto,
    com cálculo explícito de `saldo_esperado` x `saldo_contado` no
    fechamento — nenhum fechamento silencioso sem conferência.
    """

    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
    ]

    conta = models.ForeignKey(
        ContaFinanceira, on_delete=models.PROTECT, related_name='fechamentos'
    )
    data = models.DateField()
    saldo_abertura = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_esperado = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    saldo_contado = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    diferenca = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    motivo_diferenca = models.CharField(max_length=255, blank=True)

    aberto_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+'
    )
    aberto_em = models.DateTimeField(auto_now_add=True)
    fechado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
    )
    fechado_em = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberto')

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Fechamento de Caixa'
        verbose_name_plural = 'Fechamentos de Caixa'
        ordering = ['-data', '-id']
        constraints = [
            models.UniqueConstraint(
                fields=['conta'],
                condition=models.Q(status='aberto'),
                name='unico_caixa_aberto_por_conta',
            )
        ]

    def __str__(self) -> str:
        return f'Caixa {self.conta} - {self.data} ({self.get_status_display()})'


class EstornoFinanceiro(models.Model):
    """Liga um movimento original ao seu movimento inverso.

    ``movimento_original`` é OneToOne (não ForeignKey) propositalmente: isso
    impede, no nível de banco, que o mesmo movimento original seja estornado
    duas vezes — não é apenas uma checagem em Python.
    """

    movimento_original = models.OneToOneField(
        MovimentoFinanceiro, on_delete=models.PROTECT, related_name='estorno'
    )
    movimento_estorno = models.OneToOneField(
        MovimentoFinanceiro, on_delete=models.PROTECT, related_name='estorno_de'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+'
    )
    motivo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Estorno Financeiro'
        verbose_name_plural = 'Estornos Financeiros'
        ordering = ['-criado_em']

    def __str__(self) -> str:
        return f'Estorno de movimento #{self.movimento_original_id}'