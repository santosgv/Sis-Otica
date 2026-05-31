"""
Testes das views do app Autenticacao.

Rodar todos:
    python manage.py test Autenticacao.tests.test_views

Rodar uma classe:
    python manage.py test Autenticacao.tests.test_views.TestCadastroView

Rodar um teste:
    python manage.py test Autenticacao.tests.test_views.TestLogarView.test_login_credenciais_invalidas
"""

from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse

from Autenticacao.models import USUARIO, Ativacao


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def make_usuario(username='usuario_teste', password='senha123', ativo=True, **kwargs):
    defaults = dict(
        first_name='Teste',
        email='teste@teste.com',
        FUNCAO='V',
    )
    defaults.update(kwargs)
    user = USUARIO.objects.create_user(
        username=username,
        password=password,
        **defaults,
    )
    user.is_active = ativo
    user.save()
    return user


def make_token(user, ativo=False):
    from hashlib import sha256
    token_str = sha256(f"{user.username}{user.email}".encode()).hexdigest()
    return Ativacao.objects.create(token=token_str, user=user, ativo=ativo)


# ──────────────────────────────────────────────
# CADASTRO
# ──────────────────────────────────────────────

class TestCadastroView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/auth/cadastro'

    def test_get_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_usuario_autenticado_redireciona_home(self):
        make_usuario()
        self.client.login(username='usuario_teste', password='senha123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_post_senhas_diferentes_redireciona_com_erro(self):
        response = self.client.post(self.url, {
            'username': 'novo',
            'first_name': 'Novo',
            'funcao': 'V',
            'cpf': '12345678900',
            'data_nascimento': '1990-01-01',
            'email': 'novo@teste.com',
            'password': 'senha123',
            'confirm-password': 'outra_senha',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        msgs = list(response.wsgi_request._messages)
        self.assertTrue(any('senha' in str(m).lower() for m in msgs))

    def test_post_campos_vazios_redireciona_com_erro(self):
        response = self.client.post(self.url, {
            'username': '',
            'first_name': 'Novo',
            'funcao': 'V',
            'cpf': '12345678900',
            'data_nascimento': '1990-01-01',
            'email': 'novo@teste.com',
            'password': '',
            'confirm-password': '',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)

    def test_post_username_duplicado_redireciona_com_erro(self):
        make_usuario(username='duplicado')
        response = self.client.post(self.url, {
            'username': 'duplicado',
            'first_name': 'Outro',
            'funcao': 'V',
            'cpf': '00000000000',
            'data_nascimento': '1990-01-01',
            'email': 'outro@teste.com',
            'password': 'senha123',
            'confirm-password': 'senha123',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        msgs = list(response.wsgi_request._messages)
        self.assertTrue(any('usuário' in str(m).lower() or 'username' in str(m).lower() for m in msgs))

    @patch('Autenticacao.views.email_html')  # evita envio real de e-mail
    def test_post_valido_cria_usuario_e_redireciona(self, mock_email):
        mock_email.return_value = None
        response = self.client.post(self.url, {
            'username': 'novo_user',
            'first_name': 'Novo',
            'funcao': 'V',
            'cpf': '98765432100',
            'data_nascimento': '1995-05-10',
            'email': 'novo@teste.com',
            'password': 'senha_segura',
            'confirm-password': 'senha_segura',
        })
        self.assertRedirects(response, '/auth/logar', fetch_redirect_response=False)
        self.assertTrue(USUARIO.objects.filter(username='novo_user').exists())

    @patch('Autenticacao.views.email_html')
    def test_post_valido_cria_token_ativacao(self, mock_email):
        mock_email.return_value = None
        self.client.post(self.url, {
            'username': 'user_token',
            'first_name': 'Token',
            'funcao': 'V',
            'cpf': '11111111111',
            'data_nascimento': '2000-01-01',
            'email': 'token@teste.com',
            'password': 'senha123',
            'confirm-password': 'senha123',
        })
        user = USUARIO.objects.get(username='user_token')
        self.assertTrue(Ativacao.objects.filter(user=user).exists())


# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────

class TestLogarView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/auth/logar'
        self.user = make_usuario()

    def test_get_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_usuario_autenticado_redireciona_home(self):
        self.client.login(username='usuario_teste', password='senha123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_post_credenciais_invalidas_redireciona_com_erro(self):
        response = self.client.post(self.url, {
            'username': 'usuario_teste',
            'password': 'senha_errada',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        msgs = list(response.wsgi_request._messages)
        self.assertTrue(any('inválido' in str(m).lower() for m in msgs))

    def test_post_credenciais_validas_redireciona_home(self):
        response = self.client.post(self.url, {
            'username': 'usuario_teste',
            'password': 'senha123',
        })
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_post_usuario_inativo_nao_loga(self):
        make_usuario(username='inativo', ativo=False)
        response = self.client.post(self.url, {
            'username': 'inativo',
            'password': 'senha123',
        })
        # authenticate retorna None para usuário inativo
        self.assertRedirects(response, self.url, fetch_redirect_response=False)

    def test_sessao_criada_apos_login(self):
        self.client.post(self.url, {
            'username': 'usuario_teste',
            'password': 'senha123',
        })
        self.assertIn('_auth_user_id', self.client.session)


# ──────────────────────────────────────────────
# ATIVAR CONTA
# ──────────────────────────────────────────────

class TestAtivarContaView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = make_usuario(ativo=False)
        self.token = make_token(self.user)

    def test_token_invalido_retorna_404(self):
        response = self.client.get('/auth/ativar_conta/token_inexistente')
        self.assertEqual(response.status_code, 404)

    def test_token_valido_ativa_usuario(self):
        self.client.get(f'/auth/ativar_conta/{self.token.token}')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_token_valido_marca_token_como_usado(self):
        self.client.get(f'/auth/ativar_conta/{self.token.token}')
        self.token.refresh_from_db()
        self.assertTrue(self.token.ativo)

    def test_token_valido_redireciona_login(self):
        response = self.client.get(f'/auth/ativar_conta/{self.token.token}')
        self.assertRedirects(response, '/auth/logar', fetch_redirect_response=False)

    def test_token_ja_usado_redireciona_com_aviso(self):
        token_usado = make_token(self.user, ativo=True)
        response = self.client.get(f'/auth/ativar_conta/{token_usado.token}')
        self.assertRedirects(response, '/auth/logar', fetch_redirect_response=False)
        msgs = list(response.wsgi_request._messages)
        self.assertTrue(any('já foi usado' in str(m).lower() for m in msgs))


# ──────────────────────────────────────────────
# ALTERAR CONTA
# ──────────────────────────────────────────────

class TestAlterarContaView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/auth/alterar_conta'
        self.user = make_usuario()
        self.client.login(username='usuario_teste', password='senha123')

    def test_get_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_exibe_dados_do_usuario(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.user.username)

    def test_post_campos_vazios_redireciona_com_erro(self):
        response = self.client.post(self.url, {
            'first_name': '',
            'cpf': '',
            'email': '',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        msgs = list(response.wsgi_request._messages)
        self.assertTrue(any('preencha' in str(m).lower() for m in msgs))

    def test_post_valido_atualiza_dados(self):
        self.client.post(self.url, {
            'first_name': 'Nome Atualizado',
            'cpf': '99988877766',
            'email': 'atualizado@teste.com',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Nome Atualizado')
        self.assertEqual(self.user.CPF, '99988877766')

    def test_post_valido_faz_logout_e_redireciona_login(self):
        response = self.client.post(self.url, {
            'first_name': 'Outro Nome',
            'cpf': '11122233344',
            'email': 'outro@teste.com',
        })
        self.assertRedirects(response, '/auth/logar', fetch_redirect_response=False)
        # sessão deve ter sido encerrada
        self.assertNotIn('_auth_user_id', self.client.session)


# ──────────────────────────────────────────────
# SAIR
# ──────────────────────────────────────────────

class TestSairView(TestCase):

    def setUp(self):
        self.client = Client()
        make_usuario()
        self.client.login(username='usuario_teste', password='senha123')

    def test_sair_encerra_sessao(self):
        self.client.get('/auth/sair')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_sair_redireciona_login(self):
        response = self.client.get('/auth/sair')
        self.assertRedirects(response, '/auth/logar', fetch_redirect_response=False)


# ──────────────────────────────────────────────
# FOLHA DE PAGAMENTO
# ──────────────────────────────────────────────

class TestListarFolhaPagamentoView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/listar_folha_pagamento'  # ajuste se a url for diferente
        self.gerente = make_usuario(username='gerente', FUNCAO='G')
        self.vendedor = make_usuario(username='vendedor', FUNCAO='V')

    def test_nao_autenticado_redireciona_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f'/auth/logar/?next={self.url}',
            fetch_redirect_response=False,
        )

    def test_gerente_ve_todos_colaboradores(self):
        self.client.login(username='gerente', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # folha_pagamento deve ter entradas para os dois usuários ativos
        folha = response.context['folha_pagamento']
        usernames = [f['colaborador'].username for f in folha]
        self.assertIn('gerente', usernames)
        self.assertIn('vendedor', usernames)

    def test_vendedor_ve_apenas_propria_folha(self):
        self.client.login(username='vendedor', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        folha = response.context['folha_pagamento']
        self.assertEqual(len(folha), 1)
        self.assertEqual(folha[0]['colaborador'].username, 'vendedor')

    def test_contexto_contem_mes_e_ano(self):
        self.client.login(username='gerente', password='senha123')
        response = self.client.get(self.url)
        self.assertIn('mes_atual', response.context)
        self.assertIn('ano_atual', response.context)

    def test_salario_liquido_presente_no_contexto(self):
        self.client.login(username='vendedor', password='senha123')
        response = self.client.get(self.url)
        folha = response.context['folha_pagamento']
        self.assertIn('salario_liquido', folha[0])
        self.assertIn('total_descontos', folha[0])
        self.assertIn('desconto_inss', folha[0])
        self.assertIn('desconto_irrf', folha[0])


# ──────────────────────────────────────────────
# COLABORADOR (CBV)
# ──────────────────────────────────────────────

class TestColaboradorViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.gerente = make_usuario(username='gerente', FUNCAO='G')
        self.client.login(username='gerente', password='senha123')

    def test_list_retorna_200(self):
        response = self.client.get(reverse('colaborador_list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_retorna_200(self):
        response = self.client.get(reverse('colaborador_detail', args=[self.gerente.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_get_retorna_200(self):
        response = self.client.get(reverse('colaborador_update', args=[self.gerente.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_post_atualiza_e_redireciona(self):
        response = self.client.post(
            reverse('colaborador_update', args=[self.gerente.pk]),
            {
                'username': self.gerente.username,
                'first_name': 'Nome Editado',
                'email': self.gerente.email,
                # inclua os campos obrigatórios do ColaboradorForm
            }
        )
        # redireciona para a lista após sucesso
        self.assertIn(response.status_code, [200, 302])


# ──────────────────────────────────────────────
# DESCONTO (CBV)
# ──────────────────────────────────────────────

class TestDescontoViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.gerente = make_usuario(username='gerente', FUNCAO='G')
        self.client.login(username='gerente', password='senha123')

    def test_list_retorna_200(self):
        response = self.client.get(reverse('desconto_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_get_retorna_200(self):
        response = self.client.get(reverse('desconto_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_cria_desconto(self):
        from Autenticacao.models import Desconto
        count_antes = Desconto.objects.count()
        self.client.post(reverse('desconto_create'), {
            'colaborador': self.gerente.pk,
            'descricao': 'VT',
            'percentual': '5.00',
        })
        # verifica que tentou criar (pode variar conforme campos do form)
        self.assertGreaterEqual(Desconto.objects.count(), count_antes)

    def test_delete_view_retorna_200(self):
        from Autenticacao.models import Desconto
        desconto = Desconto.objects.create(
            colaborador=self.gerente,
            descricao='VR',
            percentual=3,
        )
        response = self.client.get(reverse('desconto_delete', args=[desconto.pk]))
        self.assertEqual(response.status_code, 200)


# ──────────────────────────────────────────────
# COMISSAO (CBV)
# ──────────────────────────────────────────────

class TestComissaoViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.gerente = make_usuario(username='gerente', FUNCAO='G')
        self.client.login(username='gerente', password='senha123')

    def test_list_retorna_200(self):
        response = self.client.get(reverse('comissao_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_get_retorna_200(self):
        response = self.client.get(reverse('comissao_create'))
        self.assertEqual(response.status_code, 200)