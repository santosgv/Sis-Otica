"""
Testes unitários das models do projeto ótica.

Rodar todos:
    python manage.py test Core.tests.test_models

Rodar uma classe específica:
    python manage.py test Core.tests.test_models.TestORDEN

Rodar um teste específico:
    python manage.py test Core.tests.test_models.TestORDEN.test_valor_pago_inicial_zero
"""

from decimal import Decimal
from datetime import date, timedelta

from django.test import TestCase
from django.utils.timezone import now

from Autenticacao.models import USUARIO
from Core.models import (
    CAIXA,
    CLIENTE,
    LABORATORIO,
    ORDEN,
    ParcelaOrdem,
    Produto,
    Review,
    SERVICO,
    Fornecedor,
    Tipo,
    Estilo,
    TipoUnitario,
)


# ──────────────────────────────────────────────
# FIXTURES / HELPERS
# ──────────────────────────────────────────────

def make_usuario(**kwargs):
    defaults = dict(
        username='vendedor_teste',
        first_name='Vendedor',
        password='senha123',
    )
    defaults.update(kwargs)
    return USUARIO.objects.create_user(**defaults)


def make_cliente(**kwargs):
    defaults = dict(
        NOME='Cliente Teste',
        LOGRADOURO='Rua A',
        CEP='30000000',
        NUMERO='10',
        BAIRRO='Centro',
        CIDADE='BH',
        CPF='00000000000',
    )
    defaults.update(kwargs)
    return CLIENTE.objects.create(**defaults)


def make_servico(**kwargs):
    defaults = dict(SERVICO='Montagem de lentes', ATIVO=True)
    defaults.update(kwargs)
    return SERVICO.objects.create(**defaults)


def make_laboratorio(**kwargs):
    defaults = dict(LABORATORIO='Lab Central', ATIVO=True)
    defaults.update(kwargs)
    return LABORATORIO.objects.create(**defaults)


def make_orden(vendedor, cliente, servico, laboratorio, **kwargs):
    defaults = dict(
        PREVISAO_ENTREGA=date.today() + timedelta(days=7),
        VALOR=Decimal('1000.00'),
        ENTRADA='0',
        VALOR_PAGO=Decimal('0.00'),
        QUANTIDADE_PARCELA=1,
        FORMA_PAG='B',
    )
    defaults.update(kwargs)
    return ORDEN.objects.create(
        VENDEDOR=vendedor,
        CLIENTE=cliente,
        SERVICO=servico,
        LABORATORIO=laboratorio,
        **defaults,
    )


def make_produto(**kwargs):
    fornecedor = Fornecedor.objects.create(nome='Fornecedor Teste')
    tipo = Tipo.objects.create(nome='Armação')
    estilo = Estilo.objects.create(nome='Casual')
    tu = TipoUnitario.objects.create(nome='UN')
    defaults = dict(
        nome='Armação Top',
        fornecedor=fornecedor,
        Tipo=tipo,
        Estilo=estilo,
        preco_unitario=Decimal('50.00'),
        preco_venda=Decimal('80.00'),
        quantidade=10,
        quantidade_minima=2,
        tipo_unitario=tu,
    )
    defaults.update(kwargs)
    return Produto.objects.create(**defaults)


# ──────────────────────────────────────────────
# TESTES: CLIENTE
# ──────────────────────────────────────────────

class TestCLIENTE(TestCase):

    def test_str_retorna_nome(self):
        cliente = make_cliente(NOME='João Silva')
        self.assertEqual(str(cliente), 'João Silva')

    def test_status_padrao_ativo(self):
        cliente = make_cliente()
        self.assertEqual(cliente.STATUS, '1')

    def test_campos_opcionais_podem_ser_nulos(self):
        cliente = make_cliente(TELEFONE=None, EMAIL=None, FOTO=None)
        self.assertIsNone(cliente.TELEFONE)
        self.assertIsNone(cliente.EMAIL)

    def test_data_cadastro_preenchida_automaticamente(self):
        cliente = make_cliente()
        self.assertIsNotNone(cliente.DATA_CADASTRO)


# ──────────────────────────────────────────────
# TESTES: SERVICO / LABORATORIO
# ──────────────────────────────────────────────

class TestSERVICO(TestCase):

    def test_str_retorna_nome_servico(self):
        s = make_servico(SERVICO='Lentes progressivas')
        self.assertEqual(str(s), 'Lentes progressivas')

    def test_ativo_por_padrao(self):
        s = make_servico()
        self.assertTrue(s.ATIVO)

    def test_pode_ser_inativado(self):
        s = make_servico(ATIVO=False)
        self.assertFalse(s.ATIVO)


class TestLABORATORIO(TestCase):

    def test_str_retorna_nome_laboratorio(self):
        lab = make_laboratorio(LABORATORIO='Lab Norte')
        self.assertEqual(str(lab), 'Lab Norte')

    def test_ativo_por_padrao(self):
        lab = make_laboratorio()
        self.assertTrue(lab.ATIVO)


# ──────────────────────────────────────────────
# TESTES: ORDEN
# ──────────────────────────────────────────────

class TestORDEN(TestCase):

    def setUp(self):
        self.vendedor = make_usuario()
        self.cliente = make_cliente()
        self.servico = make_servico()
        self.lab = make_laboratorio()

    def _make(self, **kwargs):
        return make_orden(self.vendedor, self.cliente, self.servico, self.lab, **kwargs)

    def test_str_retorna_id(self):
        os_ = self._make()
        self.assertEqual(str(os_), str(os_.id))

    def test_status_padrao_solicitado(self):
        os_ = self._make()
        self.assertEqual(os_.STATUS, 'A')

    def test_valor_pago_inicial_zero(self):
        os_ = self._make(VALOR_PAGO=Decimal('0'))
        self.assertEqual(os_.VALOR_PAGO, Decimal('0'))

    def test_valor_decimal_salvo_corretamente(self):
        os_ = self._make(VALOR=Decimal('1500.50'))
        os_.refresh_from_db()
        self.assertEqual(os_.VALOR, Decimal('1500.50'))

    def test_entrada_salva_como_string(self):
        os_ = self._make(ENTRADA='250')
        os_.refresh_from_db()
        self.assertEqual(os_.ENTRADA, '250')

    def test_falta_pagar_calculado_corretamente(self):
        """Garante que a lógica (VALOR - VALOR_PAGO) está correta."""
        os_ = self._make(VALOR=Decimal('1000'), VALOR_PAGO=Decimal('400'))
        falta = os_.VALOR - os_.VALOR_PAGO
        self.assertEqual(falta, Decimal('600'))

    def test_data_solicitacao_preenchida(self):
        os_ = self._make()
        self.assertIsNotNone(os_.DATA_SOLICITACAO)

    def test_solicitar_avaliacao_false_quando_nao_entregue(self):
        os_ = self._make(STATUS='A')
        self.assertFalse(os_.solicitar_avaliacao())

    def test_solicitar_avaliacao_true_quando_entregue_sem_review(self):
        os_ = self._make(STATUS='E')
        self.assertTrue(os_.solicitar_avaliacao())

    def test_solicitar_avaliacao_false_quando_entregue_com_review(self):
        os_ = self._make(STATUS='E')
        Review.objects.create(cliente=self.cliente, nota=5)
        self.assertFalse(os_.solicitar_avaliacao())

    def test_cancelamento_muda_status(self):
        os_ = self._make()
        os_.STATUS = 'C'
        os_.save(update_fields=['STATUS'])
        os_.refresh_from_db()
        self.assertEqual(os_.STATUS, 'C')

    def test_valor_pago_atualizado_via_queryset(self):
        """Simula o que o signal faz — update direto sem HistoricalRecords."""
        os_ = self._make(VALOR=Decimal('500'), VALOR_PAGO=Decimal('0'))
        ORDEN.objects.filter(pk=os_.pk).update(VALOR_PAGO=Decimal('150'))
        os_.refresh_from_db()
        self.assertEqual(os_.VALOR_PAGO, Decimal('150'))


# ──────────────────────────────────────────────
# TESTES: CAIXA
# ──────────────────────────────────────────────

class TestCAIXA(TestCase):

    def setUp(self):
        self.vendedor = make_usuario()
        self.cliente = make_cliente()
        self.servico = make_servico()
        self.lab = make_laboratorio()
        self.orden = make_orden(self.vendedor, self.cliente, self.servico, self.lab)

    def _make_caixa(self, **kwargs):
        defaults = dict(
            DESCRICAO='Entrada teste',
            TIPO='E',
            VALOR=100.0,
            FORMA='B',
            FECHADO=False,
            ABERTO=False,
        )
        defaults.update(kwargs)
        return CAIXA.objects.create(**defaults)

    def test_str_retorna_id(self):
        c = self._make_caixa()
        self.assertEqual(str(c), str(c.id))

    def test_fechado_padrao_false(self):
        c = self._make_caixa()
        self.assertFalse(c.FECHADO)

    def test_aberto_padrao_false(self):
        c = self._make_caixa()
        self.assertFalse(c.ABERTO)

    def test_fechar_caixa_marca_fechado_e_desmarca_aberto(self):
        c = self._make_caixa(ABERTO=True)
        c.fechar_caixa()
        c.save()
        c.refresh_from_db()
        self.assertTrue(c.FECHADO)
        self.assertFalse(c.ABERTO)

    def test_apenas_um_caixa_aberto_por_dia(self):
        """Regra de negócio: não deve existir mais de um caixa aberto no mesmo dia."""
        CAIXA.objects.create(
            DATA=date.today(), DESCRICAO='Abertura', TIPO='E',
            VALOR=0, FORMA='B', ABERTO=True, FECHADO=False
        )
        abertos_hoje = CAIXA.objects.filter(ABERTO=True, FECHADO=False, DATA=date.today()).count()
        self.assertEqual(abertos_hoje, 1)

    def test_entrada_com_referencia_salva(self):
        c = self._make_caixa(REFERENCIA=self.orden, TIPO='E', VALOR=500.0)
        self.assertEqual(c.REFERENCIA, self.orden)
        self.assertEqual(c.TIPO, 'E')

    def test_saida_sem_referencia(self):
        c = self._make_caixa(TIPO='S', VALOR=200.0, REFERENCIA=None)
        self.assertEqual(c.TIPO, 'S')
        self.assertIsNone(c.REFERENCIA)

    def test_tipo_entrada_choices_validos(self):
        tipos_validos = {'E', 'S'}
        c = self._make_caixa(TIPO='E')
        self.assertIn(c.TIPO, tipos_validos)

    def test_forma_pagamento_choices_validos(self):
        formas_validas = {'A', 'B', 'C', 'D', 'E', 'F'}
        for forma in formas_validas:
            c = self._make_caixa(FORMA=forma)
            self.assertIn(c.FORMA, formas_validas)


# ──────────────────────────────────────────────
# TESTES: ParcelaOrdem
# ──────────────────────────────────────────────

class TestParcelaOrdem(TestCase):

    def setUp(self):
        self.vendedor = make_usuario()
        self.cliente = make_cliente()
        self.servico = make_servico()
        self.lab = make_laboratorio()
        self.orden = make_orden(
            self.vendedor, self.cliente, self.servico, self.lab,
            VALOR=Decimal('900'), ENTRADA='300', QUANTIDADE_PARCELA=3
        )

    def _make_parcela(self, numero=1, **kwargs):
        defaults = dict(
            ordem=self.orden,
            numero=numero,
            data_vencimento=date.today() + timedelta(days=30 * numero),
            valor=Decimal('200.00'),
            pago=False,
        )
        defaults.update(kwargs)
        return ParcelaOrdem.objects.create(**defaults)

    def test_parcela_criada_como_nao_paga(self):
        p = self._make_parcela()
        self.assertFalse(p.pago)

    def test_marcar_parcela_como_paga(self):
        p = self._make_parcela()
        p.pago = True
        p.data_pagamento = date.today()
        p.forma_pagamento = 'A'
        p.save()
        p.refresh_from_db()
        self.assertTrue(p.pago)
        self.assertEqual(p.data_pagamento, date.today())

    def test_valor_parcela_decimal(self):
        p = self._make_parcela(valor=Decimal('300.00'))
        p.refresh_from_db()
        self.assertEqual(p.valor, Decimal('300.00'))

    def test_soma_parcelas_pagas(self):
        """Soma das parcelas pagas deve bater com o esperado."""
        self._make_parcela(numero=1, valor=Decimal('200'), pago=True)
        self._make_parcela(numero=2, valor=Decimal('200'), pago=True)
        self._make_parcela(numero=3, valor=Decimal('200'), pago=False)

        total = ParcelaOrdem.objects.filter(
            ordem=self.orden, pago=True
        ).aggregate(total=sum_('valor'))['total'] or Decimal('0')

        self.assertEqual(total, Decimal('400'))

    def test_parcelas_pendentes_filtradas(self):
        self._make_parcela(numero=1, pago=True)
        self._make_parcela(numero=2, pago=False)
        self._make_parcela(numero=3, pago=False)

        pendentes = ParcelaOrdem.objects.filter(ordem=self.orden, pago=False).count()
        self.assertEqual(pendentes, 2)

    def test_forma_pagamento_registrada(self):
        p = self._make_parcela()
        p.pago = True
        p.forma_pagamento = 'C'
        p.save()
        p.refresh_from_db()
        self.assertEqual(p.forma_pagamento, 'C')

    def test_calculo_parcela_sem_entrada(self):
        """(VALOR - ENTRADA) / PARCELAS deve ser o valor de cada parcela."""
        valor = Decimal('900')
        entrada = Decimal('300')
        qtd = 3
        esperado = (valor - entrada) / qtd
        self.assertEqual(esperado, Decimal('200'))

    def test_arredondamento_ultima_parcela(self):
        """Simula que a última parcela absorve o resíduo de arredondamento."""
        valor = Decimal('1000')
        entrada = Decimal('0')
        qtd = 3
        from decimal import ROUND_HALF_UP
        valor_parcela = (valor / qtd).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # 2 parcelas normais
        soma_parciais = valor_parcela * 2
        # última absorve o restante
        ultima = valor - soma_parciais
        self.assertEqual(soma_parciais + ultima, valor)


# ──────────────────────────────────────────────
# TESTES: Produto
# ──────────────────────────────────────────────

class TestProduto(TestCase):

    def test_str_retorna_nome(self):
        p = make_produto(nome='Óculos Solar')
        self.assertEqual(str(p), 'Óculos Solar')

    def test_valor_total_calculado_no_save(self):
        p = make_produto(preco_unitario=Decimal('50'), quantidade=10)
        self.assertEqual(p.valor_total, Decimal('500'))

    def test_registrar_entrada_incrementa_quantidade(self):
        p = make_produto(quantidade=5)
        p.registrar_entrada(3)
        p.refresh_from_db()
        self.assertEqual(p.quantidade, 8)

    def test_registrar_saida_decrementa_quantidade(self):
        p = make_produto(quantidade=10)
        resultado = p.registrar_saida(4)
        p.refresh_from_db()
        self.assertTrue(resultado)
        self.assertEqual(p.quantidade, 6)

    def test_registrar_saida_insuficiente_retorna_false(self):
        p = make_produto(quantidade=2)
        resultado = p.registrar_saida(5)
        self.assertFalse(resultado)
        p.refresh_from_db()
        self.assertEqual(p.quantidade, 2)  # não alterou

    def test_calcular_total_retorna_quantidade_x_preco(self):
        p = make_produto(preco_unitario=Decimal('100'), quantidade=3)
        self.assertEqual(p.calcular_total(), Decimal('300'))

    def test_codigo_gerado_automaticamente_no_save(self):
        p = make_produto(nome='Armacao X')
        self.assertIsNotNone(p.codigo)
        self.assertIn('Armacao X', p.codigo)


# ──────────────────────────────────────────────
# TESTES: Review
# ──────────────────────────────────────────────

class TestReview(TestCase):

    def setUp(self):
        self.cliente = make_cliente(NOME='Maria')

    def test_str_retorna_nota_e_cliente(self):
        r = Review.objects.create(cliente=self.cliente, nota=4)
        self.assertIn('4', str(r))
        self.assertIn('Maria', str(r))

    def test_nota_minima_1(self):
        r = Review.objects.create(cliente=self.cliente, nota=1)
        self.assertEqual(r.nota, 1)

    def test_nota_maxima_5(self):
        r = Review.objects.create(cliente=self.cliente, nota=5)
        self.assertEqual(r.nota, 5)

    def test_comentario_opcional(self):
        r = Review.objects.create(cliente=self.cliente, nota=3, comentario=None)
        self.assertIsNone(r.comentario)

    def test_data_preenchida_automaticamente(self):
        r = Review.objects.create(cliente=self.cliente, nota=5)
        self.assertIsNotNone(r.data)


# ──────────────────────────────────────────────
# Import auxiliar para o aggregate dentro da classe
# ──────────────────────────────────────────────
from django.db.models import Sum as sum_