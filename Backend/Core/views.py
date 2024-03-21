import os
from django.views.decorators.cache import cache_page
from django.contrib import messages
from datetime import datetime, date
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from Core.models import ORDEN,CLIENTE,CAIXA,SERVICO
from django.shortcuts import get_object_or_404
from Autenticacao.models import USUARIO
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime
from reportlab.pdfgen import canvas
import io
from django.utils.timezone import now
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from Autenticacao.urls import views
from django.conf import settings
from django.utils.timezone import now,timedelta
from django.db.models import Sum,Count,IntegerField,Case, When,Value
from django.db.models.functions import TruncMonth,ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.core.serializers import serialize
from decimal import Decimal
import logging
from django.db import transaction

logger = logging.getLogger('MyApp')


def get_today_data():
    date_now  = datetime.datetime.now().date()
    return date_now

def thirty_days_ago():
    data = get_today_data() - datetime.timedelta(days=30)
    return data

@login_required(login_url='/auth/logar/')  
def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return render(request,'home.html')


@login_required(login_url='/auth/logar/')
def clientes(request):
        cliente_lista = CLIENTE.objects.order_by('NOME').order_by('-DATA_CADASTRO').filter(STATUS=1).only('id').all().values()

        pagina = Paginator(cliente_lista, 25)

        page = request.GET.get('page')

        clientes = pagina.get_page(page)
        
        return render(request,'Cliente/clientes.html',{'clientes':clientes,
                                                        })

@transaction.atomic
@login_required(login_url='/auth/logar/')
def cadastro_cliente(request):
    if request.method == "GET":
        return render(request, 'Cliente/cadastro_cliente.html')
    else:
        NOME = request.POST.get('NOME')
        LOGRADOURO = request.POST.get('LOGRADOURO')
        NUMERO = request.POST.get('NUMERO')
        BAIRRO = request.POST.get('BAIRRO')
        CIDADE = request.POST.get('CIDADE')
        TELEFONE = request.POST.get('TELEFONE')
        CPF = request.POST.get('CPF')
        DATA_NASCIMENTO = request.POST.get('DATA_NASCIMENTO')
        EMAIL = request.POST.get('EMAIL')
             
    with transaction.atomic():
        cliente =CLIENTE(NOME=NOME,
        LOGRADOURO=LOGRADOURO,
        NUMERO=NUMERO,
        BAIRRO=BAIRRO,
        CIDADE=CIDADE,
        TELEFONE=TELEFONE,
        CPF=CPF,
        DATA_NASCIMENTO=DATA_NASCIMENTO,
        EMAIL=EMAIL)
        cliente.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso')
        return redirect('/clientes')

@login_required(login_url='/auth/logar/')
def Cliente(request,id):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id)
        return render(request,'Cliente/cliente.html',{'cliente':cliente})

@transaction.atomic
@login_required(login_url='/auth/logar/')
def Edita_cliente(request,id):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id)
        return render(request,'Cliente/edita_cliente.html',{'cliente':cliente})
    else:
        with transaction.atomic():
            cliente = CLIENTE.objects.get(id=id)
            cliente.NOME = request.POST.get('NOME')
            cliente.LOGRADOURO = request.POST.get('LOGRADOURO')
            cliente.NUMERO = request.POST.get('NUMERO')
            cliente.BAIRRO = request.POST.get('BAIRRO')
            cliente.CIDADE = request.POST.get('CIDADE')
            cliente.TELEFONE = request.POST.get('TELEFONE')
            cliente.CPF = request.POST.get('CPF')
            cliente.DATA_NASCIMENTO = request.POST.get('DATA_NASCIMENTO')
            cliente.EMAIL = request.POST.get('EMAIL')
            cliente.save()
            messages.add_message(request, constants.SUCCESS, 'Dados alterado com sucesso')
        return render(request,'Cliente/cliente.html',{'cliente':cliente})

@transaction.atomic
@login_required(login_url='/auth/logar/')
def excluir_cliente(request,id):
    with transaction.atomic():
        excluir = CLIENTE.objects.get(id=id)
        excluir.STATUS ='2'
        excluir.save()
        return redirect('/clientes')

@login_required(login_url='/auth/logar/')
def Lista_Os(request):
        Lista_os = ORDEN.objects.order_by('-id').all()

        pagina = Paginator(Lista_os, 25)

        page = request.GET.get('page')

        Ordem_servicos = pagina.get_page(page)

        return render(request,'Os/Lista_Os.html',{'Ordem_servicos':Ordem_servicos})

@transaction.atomic
@login_required(login_url='/auth/logar/')
def Cadastrar_os(request,id_cliente):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id_cliente)
        servicos = SERVICO.objects.filter(ATIVO=True).all()
        return render(request,'Os/cadastrar_os.html',{'cliente':cliente,'servicos':servicos})
    else:
        try:
            with transaction.atomic():
                if 'ANEXO' in  request.FILES:
                    ANEXO = request.FILES['ANEXO']
                else:
                    ANEXO = None
                VENDEDOR = request.POST.get('VENDEDOR')
                CLIENTE_POST = request.POST.get('CLIENTE')
                PREVISAO_ENTREGA = request.POST.get('PREVISAO_ENTREGA')
                if 'ASSINATURA' in request.FILES:
                    ASSINATURA = request.FILES['ASSINATURA']
                else:
                    ASSINATURA = None 
                SERVICO_POST =request.POST.get('SERVICO')
                OD_ESF = request.POST.get('OD_ESF')
                OD_CIL = request.POST.get('OD_CIL')
                OD_EIXO = request.POST.get('OD_EIXO')
                OE_ESF = request.POST.get('OE_ESF')
                OE_CIL = request.POST.get('OE_CIL')
                OE_EIXO = request.POST.get('OE_EIXO')
                AD = request.POST.get('AD')
                DNP = request.POST.get('DNP')
                P = request.POST.get('P')
                DPA = request.POST.get('DPA')
                DIAG = request.POST.get('DIAG')
                V = request.POST.get('V')
                H = request.POST.get('H')
                ALT = request.POST.get('ALT')
                ARM = request.POST.get('ARM')
                MONTAGEM = request.POST.get('MONTAGEM')
                LENTES = request.POST.get('LENTES')
                ARMACAO = request.POST.get('ARMACAO')
                OBSERVACAO = request.POST.get('OBSERVACAO')
                FORMA_PAG = request.POST.get('PAGAMENTO')
                valor_str = request.POST.get('VALOR').replace(".", "").replace(",", ".")
                valor = Decimal(valor_str)
                QUANTIDADE_PARCELA = request.POST.get('QUANTIDADE_PARCELA')

                if request.POST.get('ENTRADA') == '':
                    ENTRADA =0
                else:
                    ENTRADA = request.POST.get('ENTRADA')
                
                cadastrar_os = ORDEN(
                ANEXO= ANEXO,
                VENDEDOR = USUARIO.objects.get(id=VENDEDOR),
                CLIENTE = CLIENTE.objects.get(id=CLIENTE_POST),
                PREVISAO_ENTREGA= PREVISAO_ENTREGA,
                ASSINATURA =ASSINATURA,
                SERVICO= SERVICO.objects.get(id=SERVICO_POST),
                OD_ESF= OD_ESF,
                OD_CIL = OD_CIL,
                OD_EIXO = OD_EIXO,
                OE_ESF = OE_ESF,
                OE_CIL = OE_CIL,
                OE_EIXO = OE_EIXO,
                AD = AD,
                DNP = DNP,
                P = P,
                DPA = DPA,
                DIAG = DIAG,
                V = V,
                H = H,
                ALT = ALT,
                ARM = ARM,
                MONTAGEM = MONTAGEM,
                LENTES= LENTES,
                ARMACAO= ARMACAO,
                OBSERVACAO= OBSERVACAO,
                FORMA_PAG= FORMA_PAG,
                VALOR= valor,
                QUANTIDADE_PARCELA= QUANTIDADE_PARCELA,
                ENTRADA= ENTRADA )



                cadastrar_os.save()

                messages.add_message(request, constants.SUCCESS, 'O.S Cadastrado com sucesso')
                return redirect(f'/Visualizar_os/{cadastrar_os.id}')  
        except Exception as msg:
            logger.warning(msg)
            cliente = CLIENTE.objects.get(id=id_cliente)
            messages.add_message(request, constants.ERROR, 'Erro interno ao salvar a OS')
            return redirect(request,'/Lista_Os')  

@login_required(login_url='/auth/logar/')
def Visualizar_os(request,id_os):
    if request.method == "GET":
        VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
       
        return render(request,'Os/Visualizar_os.html',{'VISUALIZAR_OS':VISUALIZAR_OS,
                                                   })
    else:
        return render(request,'Os/Visualizar_os.htmll')
    

@transaction.atomic    
@login_required(login_url='/auth/logar/')
def Editar_os(request,id_os):
    if request.method == "GET":
        VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
        
        return render(request,'Os/Edita_os.html',{'VISUALIZAR_OS':VISUALIZAR_OS,
                                                   })
    else:
        with transaction.atomic():
            if 'ANEXO' in  request.FILES:
                ANEXO = request.FILES['ANEXO']
            else:
                ANEXO = None
            if 'ASSINATURA' in request.FILES:
                ASSINATURA = request.FILES['ASSINATURA']
            else:
                ASSINATURA = None
            FORMA_PAG = request.POST.get('PAGAMENTO')
            VALOR_str = request.POST.get('VALOR').replace(".", "").replace(",", ".")
            VALOR = Decimal(VALOR_str)
            QUANTIDADE_PARCELA = request.POST.get('QUANTIDADE_PARCELA')

            if request.POST.get('ENTRADA') == '':
                ENTRADA =0
            else:
                ENTRADA = request.POST.get('ENTRADA')
            VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
            if ANEXO is not None:
                VISUALIZAR_OS.ANEXO = ANEXO
            if ASSINATURA is not None:
                VISUALIZAR_OS.ASSINATURA = ASSINATURA
            VISUALIZAR_OS.ASSINATURA=ASSINATURA
            VISUALIZAR_OS.FORMA_PAG=FORMA_PAG
            VISUALIZAR_OS.VALOR=VALOR
            VISUALIZAR_OS.QUANTIDADE_PARCELA=QUANTIDADE_PARCELA
            VISUALIZAR_OS.ENTRADA=ENTRADA
            VISUALIZAR_OS.save()
            
            messages.add_message(request, constants.SUCCESS, 'O.S Editada com sucesso')
            return redirect(f'/Visualizar_os/{VISUALIZAR_OS.id}')  

@transaction.atomic 
@login_required(login_url='/auth/logar/')
def Encerrar_os(request,id_os):
    if request.method == "GET":
        try:
            with transaction.atomic():
                Encerrar_OS = ORDEN.objects.get(id=id_os)
                Encerrar_OS.STATUS = "E"
                Encerrar_OS.DARA_ENCERRAMENTO =now()
                Encerrar_OS.save()
                messages.add_message(request, constants.SUCCESS, 'O.s Encerrada com sucesso')
                return redirect('/Lista_Os')  
        except Exception as msg:
            logger.info(msg)
            return redirect('/Lista_Os')   

@transaction.atomic 
@login_required(login_url='/auth/logar/')
def Cancelar_os(request,id_os):
    if request.method == "GET":
        try:
            with transaction.atomic():
                CANCELAR_OS = ORDEN.objects.get(id=id_os)
                CANCELAR_OS.STATUS ="C"
                CANCELAR_OS.save()
                messages.add_message(request, constants.SUCCESS, 'O.s Foi Cancelada com sucesso')
                return redirect('/Lista_Os')  
        except Exception as msg:
            logger.info(msg)
            return redirect('/Lista_Os')

@transaction.atomic 
@login_required(login_url='/auth/logar/')
def Laboratorio_os(request,id_os):
    if request.method == "GET":
        try:
            with transaction.atomic():
                Laboratorio_os = ORDEN.objects.get(id=id_os)
                Laboratorio_os.STATUS ="L"
                Laboratorio_os.save()
                messages.add_message(request, constants.SUCCESS, 'O.s Foi Movido para o Laboratorio com sucesso')
                return redirect('/Lista_Os')  
        except Exception as msg:
            logger.info(msg)
            return redirect('/Lista_Os')  

@transaction.atomic 
@login_required(login_url='/auth/logar/')
def Loja_os(request,id_os):
    if request.method == "GET":
        try:
            with transaction.atomic():
                Loja_os = ORDEN.objects.get(id=id_os)
                Loja_os.STATUS ="J"
                Loja_os.save()
                messages.add_message(request, constants.SUCCESS, 'O.s Foi Movido para a Loja com sucesso')
                return redirect('/Lista_Os')  
        except Exception as msg:
            logger.info(msg)
            return redirect('/Lista_Os')      

@login_required(login_url='/auth/logar/')   
def Imprimir_os(request,id_os):
    try:
        PRINT_OS =ORDEN.objects.get(id=id_os)
        
        buffer = io.BytesIO()
        PDF = canvas.Canvas(buffer,pagesize=letter)
        PDF.setFont('Courier', 12)
        PDF.drawImage(os.path.join(settings.BASE_DIR, 'templates','OS_exemplo_page.jpg'),0, 0, width=letter[0], height=letter[1])

        PDF.drawString(136,744,str(PRINT_OS.DATA_SOLICITACAO.strftime('%d-%m-%Y')))
        PDF.drawString(325,744,(PRINT_OS.VENDEDOR.first_name))
        PDF.drawString(565,744,str(PRINT_OS.id))
        PDF.drawString(88,724,str(PRINT_OS.CLIENTE.NOME[:23]))
        PDF.drawString(385,724,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d-%m-%Y')))
        PDF.drawString(88,665,str(PRINT_OS.SERVICO))
        PDF.drawString(385,665,str('xxx'))
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
        PDF.drawString(136,423,str(PRINT_OS.DATA_SOLICITACAO.strftime('%d-%m-%Y')))
        PDF.drawString(325,423,str(PRINT_OS.VENDEDOR.first_name))
        PDF.drawString(565,423,str(PRINT_OS.id))
        PDF.drawString(88,402,str(PRINT_OS.CLIENTE.NOME[:23]))
        PDF.drawString(385,402,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d-%m-%Y')))
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
        return FileResponse(buffer, as_attachment=True, filename=f'OS-{PRINT_OS.id}.pdf')
    except Exception as msg:
        print(msg)
        logger.warning(msg)
        return redirect('/Lista_Os')

     
@login_required(login_url='/auth/logar/')
def Dashabord(request):
    Lista_os = ORDEN.objects.filter(DATA_SOLICITACAO__gte=thirty_days_ago(),DATA_SOLICITACAO__lte=get_today_data()).order_by('id').all()
    pagina = Paginator(Lista_os, 10)
    page = request.GET.get('page')
    kankan_servicos = pagina.get_page(page)
    return render(request,'dashabord/dashabord.html',{'kankan_servicos':kankan_servicos})

def dados_caixa():
    dado = CAIXA.objects.filter(DATA__gte=thirty_days_ago(),DATA__lte=get_today_data(),FECHADO=False).order_by('-id')
    return dado

def get_entrada_saida():
    entradas = CAIXA.objects.filter(DATA__gte=thirty_days_ago(),DATA__lte=get_today_data(), TIPO='E',FORMA='B',FECHADO=False).only('VALOR').all().aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    saidas = CAIXA.objects.filter(DATA__gte=thirty_days_ago(),DATA__lte=get_today_data(), TIPO='S',FORMA='B',FECHADO=False).only('VALOR').all().aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    saldo = entradas - saidas

    entradas_total = CAIXA.objects.filter(DATA__gte=thirty_days_ago(),DATA__lte=get_today_data(), TIPO='E',FECHADO=False).exclude(FORMA='B').only('VALOR').all().aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    saidas_total = CAIXA.objects.filter(DATA__gte=thirty_days_ago(),DATA__lte=get_today_data(), TIPO='S',FECHADO=False).exclude(FORMA='B').only('VALOR').all().aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    saldo_total = entradas_total - saidas_total

    return entradas,saidas,saldo,saldo_total

@login_required(login_url='/auth/logar/')
def Caixa(request):
    if request.method == "GET":
        try:
            dadoscaixa = dados_caixa()
            entradas,saida,saldo,saldo_total= get_entrada_saida()
            pagina = Paginator(dadoscaixa,15)
            page = request.GET.get('page')
            dados = pagina.get_page(page)
            return render(request,'Caixa/caixa.html',{'dados':dados,
                                                      'entrada':entradas,
                                                      'saida':saida,
                                                      'saldo':saldo,
                                                      'saldo_total':saldo_total})
        except Exception as msg:
            logger.critical(msg)
    return render(request,'Caixa/caixa.html')

@login_required(login_url='/auth/logar/')
def fechar_caixa(request):
    hora = datetime.datetime.now()
    if hora.hour >= 20:
        caixa = CAIXA.objects.filter(DATA__gte=thirty_days_ago(),DATA__lte=get_today_data(),FECHADO=False).order_by('-id')
        for dado in caixa:
            dado.fechar_caixa()
            dado.save()
        messages.add_message(request, constants.SUCCESS, 'Caixa Fechado com sucesso')
        return redirect('/Caixa')
    else:
        messages.add_message(request, constants.WARNING, 'O caixa deve ser fechado apos as 20 Horas de hoje!')
        return redirect('/Caixa')

@transaction.atomic
@login_required(login_url='/auth/logar/')
def cadastro_caixa(request):
    if request.method =="GET":
        os_disponiveis= ORDEN.objects.exclude(STATUS='C').exclude(STATUS='E').all()
        return render(request,'Caixa/caixa_fluxo.html',{
            'OsS':os_disponiveis,
            'data':get_today_data()
        })
    else:
        with transaction.atomic():
            descricao =request.POST.get('DESCRICAO')
            referencia = request.POST.get('REFERENCIA')
            tipo= request.POST.get('TIPO')
            valor_str = request.POST.get('VALOR')
            forma= request.POST.get('FORMA')

            valor_str = valor_str.replace('.', '').replace(',', '.')

            
            if referencia and referencia != 'null':
                referencia_obj = get_object_or_404(ORDEN, id=referencia)
            else:
                referencia_obj = None
            caixa = CAIXA.objects.create(
                DATA=get_today_data(),
                VALOR=valor_str,
                DESCRICAO=descricao,
                REFERENCIA= referencia_obj,
                TIPO=tipo,
                FORMA=forma
            )
            caixa.save()
            messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso')
            return redirect('/Caixa')

def vendas_ultimos_12_meses(request):
    hoje = get_today_data()
    data_limite = hoje - timedelta(days=365)

    vendas = (
        ORDEN.objects
        .annotate(mes_venda=TruncMonth('DATA_SOLICITACAO')) 
        .values('mes_venda')
        .annotate(total_vendas=Count('id'))
        .filter(DATA_SOLICITACAO__gte=data_limite).exclude(STATUS='C')
        .order_by('mes_venda')
    )

    data_vendas = [{'mes_venda': venda['mes_venda'].strftime('%m-%Y'), 'total_vendas': venda['total_vendas']} for venda in vendas]
    return JsonResponse({'data': data_vendas})

def maiores_vendedores_30_dias(request):
    vendedores = ORDEN.objects.filter(DATA_SOLICITACAO__gte=thirty_days_ago()).exclude(STATUS='C') \
        .values('VENDEDOR__first_name') \
        .annotate(total_pedidos=Count('id')) \
        .annotate(total_valor_vendas=Sum('VALOR')) \
        .order_by('-total_pedidos')[:5]
    return JsonResponse({'maiores_vendedores_30_dias': list(vendedores)})

def transacoes_mensais(request):
    # Realiza uma agregação dos valores das transações por mês e tipo
    transacoes_mensais = CAIXA.objects.annotate(
        ano=ExtractYear('DATA'),
        mes=ExtractMonth('DATA')
    ).values('ano', 'mes', 'TIPO').annotate(
        total=Sum('VALOR'),
        quantidade=Count('id')
    ).filter(FECHADO=True)

    # Cria um dicionário para armazenar os totais mensais de entradas e saídas
    dados_mensais = {}

    # Itera sobre as transações agregadas e agrupa os totais por mês, ano e tipo
    for transacao in transacoes_mensais:
        ano = transacao['ano']
        mes = transacao['mes']
        tipo = transacao['TIPO']
        total = transacao['total']
        quantidade = transacao['quantidade']

        # Verifica se já existe um registro para o mês e ano atual
        if (ano, mes) in dados_mensais:
            dados = dados_mensais[(ano, mes)]
        else:
            dados = {'entrada': {'total': 0, 'quantidade': 0}, 'saida': {'total': 0, 'quantidade': 0}}

        # Atualiza o total correspondente com base no tipo (entrada ou saída)
        if tipo == 'E':
            dados['entrada']['total'] += total
            dados['entrada']['quantidade'] += quantidade
        elif tipo == 'S':
            dados['saida']['total'] += total
            dados['saida']['quantidade'] += quantidade

        # Atualiza o dicionário de dados mensais
        dados_mensais[(ano, mes)] = dados

    # Formata os dados para a resposta JSON
    dados_formatados = [
        {
            'ano': ano,
            'mes': mes,
            'entrada': dados['entrada'],
            'saida': dados['saida'],
        }
        for (ano, mes), dados in dados_mensais.items()
    ]

    # Retorna os dados como JsonResponse
    return JsonResponse({'data': dados_formatados}, safe=False)

def caixa_mes_anterior(request):
    return render(request, 'Caixa/caixa_mes_anterior.html')

def obter_valores_registros_meses_anteriores(request):
    if request.method == "GET":
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')

        registros = CAIXA.objects.filter(
                DATA__range=(data_inicio, data_fim),
                FECHADO=True
            ).annotate(ano=ExtractYear('DATA'), mes=ExtractMonth('DATA')).values('ano', 'mes').annotate(
                total_entradas=Sum(
                    Case(
                        When(TIPO='E', then='VALOR'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ),
                quantidade_entradas=Count(
                    Case(
                        When(TIPO='E', then='VALOR')
                    )
                ),
                total_saidas=Sum(
                    Case(
                        When(TIPO='S', then='VALOR'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ),
                quantidade_saidas=Count(
                    Case(
                        When(TIPO='S', then='VALOR')
                    )
                )
            ).order_by('ano', 'mes')

        resultados = []
        for registro in registros:
            resultado = {
                    'ano': registro['ano'],
                    'mes': registro['mes'],
                    'entrada': {
                        'total': registro['total_entradas'],
                        'quantidade': registro['quantidade_entradas']
                    },
                    'saida': {
                        'total': registro['total_saidas'],
                        'quantidade': registro['quantidade_saidas']
                    }
                }
            resultados.append(resultado)
        return JsonResponse({'data': resultados})
    
def obter_os_em_aberto(request):    
    hoje = get_today_data()
    
    vendas = (
        ORDEN.objects
        .annotate(mes_venda=TruncMonth('DATA_SOLICITACAO')) 
        .values('mes_venda')
        .annotate(total_vendas=Count('id'))
        .annotate(total_valor=Sum('VALOR'))  # Adicione essa linha para calcular o valor total das vendas
        .filter(DATA_SOLICITACAO__gte=hoje)
        .exclude(STATUS='C')
        .exclude(STATUS='E')
        .order_by('mes_venda')
    )

    data_vendas = [{
        'total_vendas': venda['total_vendas'],
        'total_valor': venda['total_valor'],  # Inclua o valor total das vendas no resultado
    } for venda in vendas]

    return JsonResponse({'data':data_vendas})

@login_required(login_url='/auth/logar/')
def relatorios(request):
    return render(request,'Relatorio/relatorios.html')

@login_required(login_url='/auth/logar/')
def dados_minhas_vendas(request):
    id_user = request.user
    vendedor = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_today_data(), VENDEDOR=USUARIO.objects.get(id=id_user.id)).exclude(STATUS='C') \
        .values('VENDEDOR__first_name') \
        .annotate(total_pedidos=Count('id')) \
        .annotate(total_valor_vendas=Sum('VALOR')) \
        .order_by('-total_pedidos')[:1]
    return JsonResponse({'minhas_vendas_mes': list(vendedor)})

@login_required(login_url='/auth/logar/')
def minhas_vendas(request):
    return render(request,'minhas_vendas.html')

    