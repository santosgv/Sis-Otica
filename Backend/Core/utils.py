from urllib.parse import quote
from django.conf import settings
from Core.models import SaidaEstoque, EntradaEstoque, MovimentoEstoque,Produto,CAIXA
from datetime import datetime, date
from calendar import monthrange
import datetime
from django.http import FileResponse
import io
import os
from reportlab.lib.pagesizes import letter
from django.shortcuts import redirect
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from Core.models import ORDEN
from django.utils.timezone import timedelta
import logging

logger = logging.getLogger('MyApp')


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


def Imprimir_os(request,id_os):
    try:
        PRINT_OS =ORDEN.objects.get(id=id_os)
        
        buffer = io.BytesIO()
        PDF = canvas.Canvas(buffer,pagesize=letter)
        PDF.setFont('Courier', 12)
        PDF.drawImage(os.path.join(settings.BASE_DIR, 'templates','OS_exemplo_page.jpg'),0, 0, width=letter[0], height=letter[1])

        PDF.drawString(136,744,str(PRINT_OS.DATA_SOLICITACAO.strftime('%d-%m-%Y')))
        PDF.drawString(325,744,(PRINT_OS.VENDEDOR.first_name))
        PDF.drawString(325,778,str(settings.UNIDADE)+str(PRINT_OS.id))
        PDF.drawString(88,724,str(PRINT_OS.CLIENTE.NOME[:23]))
        PDF.drawString(385,724,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d-%m-%Y')))
        PDF.drawString(88,665,str(PRINT_OS.SERVICO))
        PDF.drawString(385,665,str('N/D'))
        PDF.drawString(88,637,str(PRINT_OS.LENTES))
        PDF.drawString(88,620,str(PRINT_OS.ARMACAO))
        PDF.drawString(109,592,str(PRINT_OS.OBSERVACAO[:69]))
        if PRINT_OS.FORMA_PAG == 'A':
            PDF.drawString(109,539,'PIX')
        elif PRINT_OS.FORMA_PAG == 'B':
            PDF.drawString(109,539,'DINHEIRO')
        elif PRINT_OS.FORMA_PAG == 'C':
            PDF.drawString(109,539,'DEBITO')
        elif PRINT_OS.FORMA_PAG == 'D':
            PDF.drawString(109,539,'CREDITO')
        elif PRINT_OS.FORMA_PAG == 'E':
            PDF.drawString(109,539,'CARNER')
        elif PRINT_OS.FORMA_PAG == 'F':
            PDF.drawString(109,539,'PERMUTA')
        
        PDF.drawString(240,539,str(PRINT_OS.VALOR))
        PDF.drawString(385,539,str(PRINT_OS.QUANTIDADE_PARCELA))
        PDF.drawString(520,539,str(PRINT_OS.ENTRADA))
        # parte laboratorio
        PDF.setFont('Courier-Bold', 12)
        PDF.drawString(325,454,str(settings.UNIDADE)+str(PRINT_OS.id))
        PDF.drawString(395,454,str(settings.NOME))
        PDF.drawString(136,405,str(PRINT_OS.DATA_SOLICITACAO.strftime('%d-%m-%Y')))
        PDF.drawString(325,405,str(PRINT_OS.VENDEDOR.first_name))
        PDF.drawString(88,385,str(PRINT_OS.CLIENTE.NOME[:23]))
        PDF.drawString(385,385,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d-%m-%Y')))
        PDF.drawString(88,361,str(PRINT_OS.SERVICO))
        PDF.drawString(338,361,str('N/D'))
        PDF.drawString(88,312,str(PRINT_OS.OD_ESF))
        PDF.drawString(88,282,str(PRINT_OS.OE_ESF))
        PDF.drawString(301,312,str(PRINT_OS.OD_CIL))
        PDF.drawString(301,282,str(PRINT_OS.OE_CIL))
        PDF.drawString(472,312,str(PRINT_OS.OD_EIXO))
        PDF.drawString(472,282,str(PRINT_OS.OE_EIXO))
        PDF.drawString(64,248,str(PRINT_OS.AD))
        PDF.drawString(78,215,str(PRINT_OS.LENTES))
        PDF.drawString(78,197,str(PRINT_OS.ARMACAO))
        PDF.drawString(109,178,str(PRINT_OS.OBSERVACAO[:69]))

        PDF.drawString(60,116,str(PRINT_OS.DNP))
        PDF.drawString(270,116,str(PRINT_OS.P))
        PDF.drawString(430,116,str(PRINT_OS.DPA))
        PDF.drawString(66,96,str(PRINT_OS.DIAG))
        PDF.drawString(270,96,str(PRINT_OS.V))
        PDF.drawString(415,96,str(PRINT_OS.H))
        PDF.drawString(60,80,str(PRINT_OS.ALT))
        PDF.drawString(432,78,str(PRINT_OS.ARM))
        PDF.drawString(94,60,str(PRINT_OS.MONTAGEM))

        PDF.showPage()
        PDF.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'OS-{settings.UNIDADE}{PRINT_OS.id}.pdf')
    except Exception as msg:
        print(msg)
        logger.warning(msg)
        return redirect('/Lista_Os')