from urllib.parse import quote
from decouple import config
import pandas as pd
from django.conf import settings
from django.db.models import Sum
from Core.models import SaidaEstoque, EntradaEstoque, MovimentoEstoque,Produto,CAIXA,ORDEN,CLIENTE
from datetime import datetime, date
from calendar import monthrange
import datetime
from django.http import FileResponse,HttpResponse
import io
import os
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.utils.timezone import timedelta
import logging
from PIL import Image
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black
from pathlib import Path

logger = logging.getLogger('MyApp')

BASE_DIR = Path(__file__).resolve().parent.parent

CHAVE_PIX =config('CHAVE_PIX')

def generate_barcode_image(code):

    barcode_value = f"{code}"
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
        barcode_image = generate_barcode_image(codigo)
        barcode_image_path = f"{settings.UNIDADE}barcode_{codigo}.png"
        
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

def get_10_days():
    dez_dias_atras = datetime.datetime.now().date() - timedelta(days=10)
    return dez_dias_atras

def get_30_days():
    dez_dias_atras = datetime.datetime.now().date() - timedelta(days=30)
    return dez_dias_atras

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

        PDF.drawString(136,744,str(PRINT_OS.DATA_SOLICITACAO.strftime('%d/%m/%Y')))
        PDF.drawString(325,744,(PRINT_OS.VENDEDOR.first_name))
        PDF.drawString(325,778,str(settings.UNIDADE)+str(PRINT_OS.id))
        PDF.drawString(88,724,str(PRINT_OS.CLIENTE.NOME[:23]))
        PDF.drawString(385,724,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d/%m/%Y')))
        PDF.drawString(88,665,str(PRINT_OS.SERVICO))
        PDF.drawString(385,665,str(PRINT_OS.LABORATORIO))
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
        PDF.drawString(136,405,str(PRINT_OS.DATA_SOLICITACAO.strftime('%d/%m/%Y')))
        PDF.drawString(325,405,str(PRINT_OS.VENDEDOR.first_name))
        PDF.drawString(88,385,str(PRINT_OS.CLIENTE.NOME[:23]))
        PDF.drawString(385,385,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d/%m/%Y')))
        PDF.drawString(88,361,str(PRINT_OS.SERVICO))
        PDF.drawString(338,361,str(PRINT_OS.LABORATORIO))
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
        'F':'FINALIZADO',
        }
        
        os = ORDEN.objects.select_related('VENDEDOR','CLIENTE','SERVICO').values(
        'id','DATA_SOLICITACAO','VENDEDOR__first_name','CLIENTE__NOME','CLIENTE__TELEFONE','SERVICO__SERVICO','LENTES',
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

def gerar_relatorio_estoque_conferido(request):
    # Crie um buffer para armazenar o PDF em memória
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Configurações iniciais
    largura_pagina, altura_pagina = letter
    y_inicial = altura_pagina - inch  # Posição inicial no topo da página
    espacamento_linha = 15  # Espaço entre linhas
    margem_esquerda = inch
    
    # Cabeçalho do PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawString(margem_esquerda, y_inicial, "Relatório de Estoque - Produtos Conferidos")
    p.setFont("Helvetica", 10)
    p.drawString(margem_esquerda, y_inicial - 20, f"Data: {date.today().strftime('%d/%m/%Y')}")

    y_posicao = y_inicial - 40

    # Cabeçalho da Tabela
    p.setFont("Helvetica-Bold", 10)
    p.drawString(margem_esquerda, y_posicao, "Código")
    p.drawString(margem_esquerda + 100, y_posicao, "Nome")
    p.drawString(margem_esquerda + 220, y_posicao, "Quantidade")
    p.drawString(margem_esquerda + 300, y_posicao, "Preço Unitário")
    p.drawString(margem_esquerda + 400, y_posicao, "Valor Total")
    
    # Traçar uma linha abaixo do cabeçalho
    y_posicao -= espacamento_linha
    p.line(margem_esquerda, y_posicao, largura_pagina - inch, y_posicao)
    y_posicao -= espacamento_linha

    # Obtenha todos os produtos conferidos
    produtos_conferidos = Produto.objects.filter(conferido=True).filter(quantidade__gt=0)
    valor_total = Produto.objects.filter(conferido=True).aggregate(Sum('valor_total'))
    quantidade = Produto.objects.filter(conferido=True).aggregate(quantidade=Sum('quantidade'))
    
    # Preenchendo as linhas com dados dos produtos conferidos
    for produto in produtos_conferidos:
        if y_posicao < inch:
            p.showPage()  # Adiciona uma nova página se a posição y for menor que 1 polegada
            y_posicao = altura_pagina - inch

        # Escreve cada campo do produto na linha
        p.setFont("Helvetica", 10)
        p.drawString(margem_esquerda, y_posicao, str(produto.codigo))
        p.drawString(margem_esquerda + 100, y_posicao, produto.nome)
        p.drawString(margem_esquerda + 220, y_posicao, f"x{produto.quantidade}")
        p.drawString(margem_esquerda + 300, y_posicao, f"R$ {produto.preco_unitario:.2f}")
        p.drawString(margem_esquerda + 400, y_posicao, f"R$ {produto.valor_total:.2f}")

        y_posicao -= espacamento_linha  # Move para a próxima linha

    # Espaço para a assinatura ao final da lista
    y_posicao -= espacamento_linha * 2  # Adiciona um pouco de espaço antes da assinatura
    p.setFont("Helvetica", 10)
    p.drawString(margem_esquerda, y_posicao, "_______________________________")
    p.drawString(margem_esquerda, y_posicao - 10, "Assinatura")
    p.drawString(margem_esquerda + 220, y_posicao ,f"Total {quantidade['quantidade']}")
    p.drawString(margem_esquerda + 300, y_posicao, f"Valor total R$ {valor_total['valor_total__sum']:.2f}")

    # Finaliza o PDF
    p.showPage()
    p.save()

    # Envia o PDF para o navegador
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="relatorio_estoque_conferido.pdf")

def gerar_carner_pdf(request, ordem_id):
    caminho_imagem =os.path.join(BASE_DIR ,'templates/static/home/img/Arte Ótica Popular transparência.png')
    

    ordem = get_object_or_404(ORDEN, id=ordem_id)

    imagem = ImageReader(caminho_imagem)

    # Calcula o valor das parcelas
    valor_total = float(ordem.VALOR)
    entrada = float(ordem.ENTRADA.replace(",", "."))
    quantidade_parcelas = int(ordem.QUANTIDADE_PARCELA)
    valor_parcela = (valor_total - entrada) / quantidade_parcelas
    # Cria um buffer para armazenar o PDF

    buffer = io.BytesIO()
    # Cria o objeto PDF usando o ReportLab
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Carnê de pagamentos - OS {ordem.id}")

    # Configurações iniciais
    largura, altura = letter
    margem = 25
    altura_boleto = 240
    espacamento = altura_boleto + 20  # Espaçamento entre os boletos
    posicao_y = altura - 10  # Posição inicial do primeiro boleto


    # Loop para gerar cada parcela
    for parcela_numero in range(1, quantidade_parcelas + 1):
        data_vencimento = get_today_data() +timedelta(days=30 * parcela_numero)

        if posicao_y < 100:  # Se o boleto estiver muito baixo, cria uma nova página
            pdf.showPage()
            posicao_y = altura - 100 # Reseta a posição inicial na nova página

        # Desenhando o retângulo do boleto
        pdf.setStrokeColor(black)
        pdf.rect(margem, posicao_y - altura_boleto, 570, altura_boleto, stroke=1, fill=0)

        # Linha pontilhada para destacar a parte do cliente
        pdf.setDash(3, 2)
        pdf.line(margem + 180, posicao_y - altura_boleto, margem + 180, posicao_y)
        pdf.setDash()

        # Dados do boleto
        pdf.setFont("Helvetica-Bold", 14)

        pdf.drawImage(imagem, margem + 15, posicao_y - 85, width=100, height=80, mask='auto')

        pdf.drawString(margem + 15, posicao_y - 110, "Parcela:")
        pdf.drawString(margem + 75, posicao_y - 110, str(f'{parcela_numero}/{quantidade_parcelas}'))

        pdf.drawString(margem + 15, posicao_y - 140, "Cliente:")
        pdf.drawString(margem + 75, posicao_y - 140, str(ordem.CLIENTE.NOME[:17]))

        pdf.drawString(margem + 15, posicao_y - 165, "OS:")
        pdf.drawString(margem + 45, posicao_y - 165, str(ordem.id))

        pdf.drawString(margem + 15, posicao_y - 200, "Vencimento:")
        pdf.drawString(margem + 100, posicao_y - 200, f"{data_vencimento.strftime('%d/%m/%Y')}")

        pdf.drawString(margem + 15, posicao_y - 230, "Valor:")
        pdf.drawString(margem + 65, posicao_y - 230, f"R$ {valor_parcela:.2f}")

        # Texto da parte do carnê
        pdf.drawString(margem + 200, posicao_y - 15, "Parcela:")
        pdf.drawString(margem + 265, posicao_y - 15, str(f'{parcela_numero}/{quantidade_parcelas}'))

        pdf.drawString(margem + 430, posicao_y - 15, "Valor:")
        pdf.drawString(margem + 475, posicao_y - 15, f"R$ {valor_parcela:.2f}")

        pdf.drawString(margem + 200, posicao_y - 45, "Carnê de pagamentos")
        pdf.drawString(margem + 200, posicao_y - 140, "Nome:")
        pdf.drawString(margem + 245, posicao_y - 140, str(ordem.CLIENTE.NOME[:24]))

        pdf.drawString(margem + 200, posicao_y - 200, "Vencimento:")
        pdf.drawString(margem + 290, posicao_y - 200, f"{data_vencimento.strftime('%d/%m/%Y')}")

        pdf.drawString(margem + 200, posicao_y - 165, "OS:")
        pdf.drawString(margem + 235, posicao_y - 165, str(ordem.id))

        pdf.drawString(margem + 200, posicao_y - 230, "Assinatura: ____________________________________")

        # Gerando o QR Code
        qr = qrcode.make(f"{CHAVE_PIX}")
        qr_img = io.BytesIO()
        qr.save(qr_img, format="PNG")
        qr_img.seek(0)

        # Adicionando QR Code no boleto
        pdf.drawImage(ImageReader(qr_img), margem + 440, posicao_y - 150, width=100, height=100, mask='auto')
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margem + 435, posicao_y - 165,"Pague com QR Code")

        # Atualiza a posição do próximo boleto
        posicao_y -= espacamento

    # Finaliza o PDF
    pdf.save()
    buffer.seek(0)

    # Retorna o PDF como resposta
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="carner_{ordem.id}.pdf"'
    return response