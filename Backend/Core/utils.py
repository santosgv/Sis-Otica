from urllib.parse import quote
import pandas as pd
from django.conf import settings
from Core.models import SaidaEstoque, EntradaEstoque, MovimentoEstoque,Produto,CAIXA
from datetime import datetime, date
from calendar import monthrange
import datetime
from django.http import FileResponse,HttpResponse
import io
import os
from reportlab.lib.pagesizes import letter
from django.shortcuts import redirect
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from Core.models import ORDEN,CLIENTE
from django.utils.timezone import timedelta
import logging
from PIL import Image
from barcode import Code128
from barcode.writer import ImageWriter
from django_tenants.utils import get_tenant_model

logger = logging.getLogger('MyApp')

def get_tenant(request):
    TenantModel = get_tenant_model()
    tenant = TenantModel.objects.get(schema_name=request.tenant.schema_name)
    return tenant

def generate_barcode_image(code, volume):

    barcode_value = f"{code}-{volume}"
    barcode = Code128(barcode_value, writer=ImageWriter())
    
    # Generate barcode image in memory
    output = io.BytesIO()
    barcode.write(output, {
        'module_height': 6.0,  # Ajustado para ficar proporcional na área de 30mm
        'module_width': 0.2,
        'quiet_zone': 6.5,
        'text_distance': 3.5,
        'font_size': 8,  # Tamanho de fonte ajustado
        'background': 'white',
        'foreground': 'black'
    })
    output.seek(0)
    return Image.open(output)

# Função para criar o PDF das etiquetas
def create_pdf(request, codigo, quantidade):
    produto_preco = Produto.objects.get(codigo=codigo)
    # Define o tamanho da etiqueta: 90mm de largura por 12mm de altura
    etiqueta_width = 90 * mm
    etiqueta_height = 12 * mm

    # Buffer de saída para o PDF
    buffer = io.BytesIO()
    
    # Cria o canvas no tamanho da etiqueta
    c = canvas.Canvas(buffer, pagesize=(etiqueta_width, etiqueta_height))

    # Configurações de layout
    labels_per_page = 10  # Ajustável dependendo da lógica de impressão
    x_inicial = 0
    y_inicial = etiqueta_height
    
    # Lógica para cada etiqueta
    for volume in range(1, quantidade + 1):
        # Gera a imagem do código de barras
        barcode_image = generate_barcode_image(codigo, volume)
        barcode_image_path = f"{settings.UNIDADE}barcode_{codigo}-{volume}.png"
        
        # Salva a imagem temporariamente
        barcode_image.save(barcode_image_path, "PNG")
        
        # Desenhar espaço em branco (primeiros 30mm)
        c.setFillColor("white")
        c.rect(x_inicial, y_inicial - 12 * mm, 30 * mm, etiqueta_height, stroke=0, fill=1)
        
        # Desenhar a informação do preço (segundo bloco de 30mm)
        c.setFillColor("black")
        c.setFont("Helvetica", 8)
        c.drawImage(barcode_image_path, x_inicial + 35 * mm, y_inicial - 13 * mm, width=30 * mm, height=11 * mm)
        # emissao de etiqueta com valor e nome do sistema
        #c.drawString(x_inicial + 35 * mm, y_inicial - 5 * mm, f"SGO SISTEMAS")
        #c.drawString(x_inicial + 35 * mm, y_inicial - 10 * mm, f"Preço: R$ {produto_preco.preco_venda}")
        
        # Desenhar o código de barras no último bloco de 30mm
        c.drawImage(barcode_image_path, x_inicial + 60 * mm, y_inicial - 13 * mm, width=30 * mm, height=11 * mm)
        
        # Movimentação para a próxima etiqueta
        x_inicial = 0
        c.showPage()  # Nova etiqueta, já que cada página é uma etiqueta

        # Remover o arquivo de imagem temporário
        os.remove(barcode_image_path)
    
    # Finaliza o PDF
    c.save()
    buffer.seek(0)

    # Retorna o PDF gerado
    return FileResponse(buffer, as_attachment=True, filename=f'etiquetas_{codigo}.pdf')

def criar_mensagem_parabens(request,cliente):
    nome_cliente = cliente
    mensagem = (
        f"*Parabéns pelo seu aniversário,{nome_cliente}!*\n\n"
        f"A *{get_tenant(request).razao_social}* deseja a você um dia repleto de alegria, amor e saúde. E para tornar essa data ainda mais especial, preparamos um presente para você!\n\n"
        f"Você ganhou um *vale-presente de R$50,00* para ser usado em compras acima de R$300,00 na nossa ótica. E o melhor de tudo: esse vale é seu, mas se preferir, você pode dar de presente para alguém especial também!\n\n"
        f"Esperamos que aproveite esse mimo e continue contando com a gente para ver o mundo com mais clareza e estilo.\n\n"
        f"Com carinho,"
        f"*{get_tenant(request).razao_social}*"
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
        PDF.drawString(325,778,str(get_tenant(request).unidade)+str(PRINT_OS.id))
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
        PDF.drawString(325,454,str(get_tenant(request).unidade)+str(PRINT_OS.id))
        PDF.drawString(395,454,str(get_tenant(request)))
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
        return FileResponse(buffer, as_attachment=True, filename=f'OS-{get_tenant(request).unidade}{PRINT_OS.id}.pdf')
    except Exception as msg:
        print(msg)
        logger.warning(msg)
        return redirect('/Lista_Os')
    
def export_clientes(request):
    try:
        clientes = CLIENTE.objects.all().filter(STATUS=1).values('NOME','EMAIL','TELEFONE','CPF','DATA_NASCIMENTO','LOGRADOURO','NUMERO','BAIRRO','CIDADE')

        df = pd.DataFrame(list(clientes))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=clientes.xlsx'
        df.to_excel(response, index=False)

        return response
    except Exception as msg:
        logger.warning(msg)

def export_os(request):
    try:
        CHOICES_PAGAMENTO_DICT = {
        'A': 'PIX',
        'B': 'DINHEIRO',
        'C': 'DEBITO',
        'D': 'CREDITO',
        'E': 'CARNER',
        'F': 'PERMUTA',
        }
        CHOICES_SITUACAO_DIC ={
        'A':'SOLICITADO',
        'E':'ENTREGUE',
        'C':'CANCELADO',
        'L':'LABORATÓRIO',
        'J':'LOJA',
        }
        
        os = ORDEN.objects.select_related('VENDEDOR','CLIENTE','SERVICO').values(
        'id','DATA_SOLICITACAO','VENDEDOR__first_name','CLIENTE__NOME','SERVICO__SERVICO','LENTES',
        'ARMACAO','OBSERVACAO','FORMA_PAG','VALOR','QUANTIDADE_PARCELA','ENTRADA','STATUS')
        df = pd.DataFrame(list(os))
        df['FORMA_PAG'] = df['FORMA_PAG'].map(CHOICES_PAGAMENTO_DICT)
        df['STATUS'] = df['STATUS'].map(CHOICES_SITUACAO_DIC)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=OS.xlsx'
        df.to_excel(response, index=False)
        return response
    except Exception as msg:
        logger.warn(msg)