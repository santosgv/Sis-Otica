from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'first_name': 'João',
            'last_name': 'Silva',
            'email': 'joao@example.com',
            'password': 'testpass123',
            'CPF': '123.456.789-09',
            'DATA_NASCIMENTO': date(1990, 5, 15),
            'FUNCAO': 'V',
            'salario_bruto': 2500.00,
            'comissao_percentual': 5.0,
            'valor_hora': 15.50,
            'data_contratacao': date(2025, 1, 10)
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'João')
        self.assertEqual(user.last_name, 'Silva')
        self.assertEqual(user.email, 'joao@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Testa a criação de um superusuário"""
        superuser_data = self.user_data.copy()
        superuser_data.update({
            'username': 'admin',
            'password': 'adminpass123',
            'is_superuser': True,
            'is_staff': True
        })
        
        user = User.objects.create_superuser(**superuser_data)
        
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_campos_personalizados(self):
        """Testa os campos personalizados do modelo"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.CPF, '123.456.789-09')
        self.assertEqual(user.DATA_NASCIMENTO, date(1990, 5, 15))
        self.assertEqual(user.STATUS, 'A')  
        self.assertEqual(user.FUNCAO, 'V')
        self.assertEqual(user.salario_bruto, 2500.00)
        self.assertEqual(user.comissao_percentual, 5.0)
        self.assertEqual(user.valor_hora, 15.50)
        self.assertEqual(user.data_contratacao, date(2025, 1, 10))

    def test_choices_situacao(self):
 
        user = User.objects.create_user(**self.user_data)
        
        situacao_choices = dict(user.CHOICES_SITUACAO)
        self.assertEqual(situacao_choices['A'], 'Ativo')
        self.assertEqual(situacao_choices['F'], 'Ferias')
        self.assertEqual(situacao_choices['I'], 'Inativo')

        self.assertEqual(user.STATUS, 'A')
        self.assertEqual(user.get_STATUS_display(), 'Ativo')

    def test_choices_funcao(self):
        user = User.objects.create_user(**self.user_data)
        
        funcao_choices = dict(user.CHOICES_FUNCAO)
        self.assertEqual(funcao_choices['V'], 'Vendedor')
        self.assertEqual(funcao_choices['C'], 'Caixa')
        self.assertEqual(funcao_choices['G'], 'Gerente')

        # Testa o valor atribuído
        self.assertEqual(user.FUNCAO, 'V')
        self.assertEqual(user.get_FUNCAO_display(), 'Vendedor')

    def test_str_representation(self):
        """Testa a representação em string do modelo"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'João')

    def test_campos_opcionais(self):
        """Testa campos que podem ser nulos ou em branco"""
        minimal_data = {
            'username': 'minimaluser',
            'password': 'minimalpass',
            'email': 'minimal@example.com'
        }
        
        user = User.objects.create_user(**minimal_data)
        self.assertIsNone(user.CPF)
        self.assertIsNone(user.DATA_NASCIMENTO)
        self.assertIsNone(user.FUNCAO)
        self.assertIsNone(user.data_contratacao)
        self.assertEqual(user.salario_bruto, 0.0)  
        self.assertEqual(user.comissao_percentual, 0.0)  
        self.assertEqual(user.valor_hora, 0.0)  

from Autenticacao.models import Ativacao, Desconto, Comissao

class AtivacaoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
    def test_create_ativacao(self):
        """Testa a criação de uma ativação"""
        ativacao = Ativacao.objects.create(
            token='1234567890abcdef',
            user=self.user,
            ativo=True
        )
        
        self.assertEqual(ativacao.token, '1234567890abcdef')
        self.assertEqual(ativacao.user, self.user)
        self.assertTrue(ativacao.ativo)
        
    def test_default_ativo_value(self):
        """Testa se o valor padrão de ativo é False"""
        ativacao = Ativacao.objects.create(
            token='1234567890abcdef',
            user=self.user
        )
        
        self.assertFalse(ativacao.ativo)
        
    def test_str_representation(self):
        """Testa a representação em string do modelo"""
        ativacao = Ativacao.objects.create(
            token='1234567890abcdef',
            user=self.user
        )
        
        self.assertEqual(str(ativacao), str(self.user))


class DescontoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='colaborador',
            password='testpass123',
            email='colab@example.com',
            first_name='Colaborador',
            last_name='Teste'
        )
        
    def test_create_desconto(self):
        """Testa a criação de um desconto"""
        desconto = Desconto.objects.create(
            colaborador=self.user,
            tipo='Vale Transporte',
            percentual=6.0
        )
        
        self.assertEqual(desconto.colaborador, self.user)
        self.assertEqual(desconto.tipo, 'Vale Transporte')
        self.assertEqual(desconto.percentual, 6.0)
        
    def test_str_representation(self):
        """Testa a representação em string do modelo"""
        desconto = Desconto.objects.create(
            colaborador=self.user,
            tipo='Vale Transporte',
            percentual=6.0
        )
        
        expected_str = f"Vale Transporte - {self.user.first_name}"
        self.assertEqual(str(desconto), expected_str)


class ComissaoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='vendedor',
            password='testpass123',
            email='vendedor@example.com',
            first_name='Vendedor',
            last_name='Teste',
            comissao_percentual=5.0,
            valor_hora=20.0
        )
        
    def test_create_comissao(self):
        """Testa a criação de uma comissão"""
        comissao = Comissao.objects.create(
            colaborador=self.user,
            valor_vendas=10000.0,
            data_referencia=date(2023, 6, 1),
            horas_extras=5.0
        )
        
        self.assertEqual(comissao.colaborador, self.user)
        self.assertEqual(comissao.valor_vendas, 10000.0)
        self.assertEqual(comissao.data_referencia, date(2023, 6, 1))
        self.assertEqual(comissao.horas_extras, 5.0)
        
    def test_calcular_comissao(self):
        """Testa o método calcular_comissao"""
        comissao = Comissao.objects.create(
            colaborador=self.user,
            valor_vendas=10000.0,
            data_referencia=date(2023, 6, 1)
        )
        
        expected_comissao = 10000.0 * (5.0 / 100)  # 5% de 10000
        self.assertEqual(comissao.calcular_comissao(), expected_comissao)
        
    def test_calcula_horas_extras(self):
        """Testa o método calcula_horas_extras"""
        comissao = Comissao.objects.create(
            colaborador=self.user,
            valor_vendas=10000.0,
            data_referencia=date(2023, 6, 1),
            horas_extras=5.0
        )
        
        # valor_hora * 1.5 * horas_extras = 20 * 1.5 * 5 = 150
        expected_valor = 20.0 * 1.5 * 5.0
        self.assertEqual(comissao.calcula_horas_extras(), expected_valor)
        
    def test_str_representation(self):
        """Testa a representação em string do modelo"""
        comissao = Comissao.objects.create(
            colaborador=self.user,
            valor_vendas=10000.0,
            data_referencia=date(2023, 6, 1)
        )
        
        expected_str = f"Comissão - {self.user.username} - 2023-06-01"
        self.assertEqual(str(comissao), expected_str)
        
    def test_horas_extras_default_value(self):
        """Testa o valor padrão de horas_extras"""
        comissao = Comissao.objects.create(
            colaborador=self.user,
            valor_vendas=10000.0,
            data_referencia=date(2023, 6, 1)
        )
        
        self.assertEqual(comissao.horas_extras, 0.0)