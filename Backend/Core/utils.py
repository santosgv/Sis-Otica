from urllib.parse import quote
from django.conf import settings
from Core.models import SaidaEstoque, EntradaEstoque, MovimentoEstoque,Produto,CAIXA
from datetime import datetime, date
from calendar import monthrange
import datetime
from django.utils.timezone import timedelta


def criar_mensagem_parabens(cliente):
    nome_cliente = cliente
    mensagem = (
        f"*Parabéns pelo seu aniversário,{nome_cliente}!*\n\n"
        f"A *{settings.NOME}* deseja a você um dia repleto de alegria, amor e saúde. E para tornar essa data ainda mais especial, preparamos um presente para você!\n\n"
        f"Você ganhou um *vale-presente de R$50,00* para ser usado em compras acima de R$300,00 na nossa ótica. E o melhor de tudo: esse vale é seu, mas se preferir, você pode dar de presente para alguém especial também!\n\n"
        f"Esperamos que aproveite esse mimo e continue contando com a gente para ver o mundo com mais clareza e estilo.\n\n"
        f"Com carinho,"
        f"*{settings.NOME}*"
    )
    return quote(mensagem)

def realizar_entrada(produto_id, quantidade):
    produto = Produto.objects.get(pk=produto_id)
    entrada_estoque = EntradaEstoque.objects.create(produto=produto, quantidade=quantidade)
    produto.registrar_entrada(quantidade)
    MovimentoEstoque.objects.create(produto=produto, tipo='E', quantidade=quantidade)
    return entrada_estoque

def realizar_saida(codigo, quantidade, observacao):
    try:
        produto = Produto.objects.get(codigo=codigo)
        
        registro_saida = produto.registrar_saida(quantidade)
        
        if registro_saida:
            MovimentoEstoque.objects.create(produto=produto, tipo='S', quantidade=quantidade)
            saida_estoque = SaidaEstoque.objects.create(produto=produto, quantidade=quantidade, observacao=observacao)
            return saida_estoque
        else:  
            return False  

    except Produto.DoesNotExist:
        return False 

def get_today_data():
    date_now  = datetime.datetime.now().date()
    return date_now

def primeiro_dia_mes():
    data_atual = date.today()
    primeiro_dia = data_atual.replace(day=1)
    return primeiro_dia

def ultimo_dia_mes():
    data_atual = date.today()
    last_date = data_atual.replace(day=1) + timedelta(monthrange(data_atual.year, data_atual.month)[1] - 1)
    return last_date

def dados_caixa():
    dado = CAIXA.objects.filter(DATA__gte=primeiro_dia_mes(),DATA__lte=ultimo_dia_mes(),FECHADO=False).order_by('-id')
    return dado
