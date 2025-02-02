
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from Core.models import LABORATORIO,ORDEN,CLIENTE,CAIXA,SERVICO,SaidaEstoque, EntradaEstoque,Fornecedor, MovimentoEstoque,TipoUnitario,Produto,Tipo,Estilo,AlertaEstoque,Estilo
from django.shortcuts import get_object_or_404
from Autenticacao.models import USUARIO
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .utils import criar_mensagem_parabens,realizar_entrada,realizar_saida,get_today_data,primeiro_dia_mes,ultimo_dia_mes,dados_caixa,get_10_days,get_30_days,get_tenant
from .utils import get_tenant,criar_mensagem_parabens,realizar_entrada,realizar_saida,get_today_data,primeiro_dia_mes,ultimo_dia_mes,dados_caixa,get_10_days,get_30_days
from django.utils.timezone import now,timedelta
from django.utils import timezone
from django.db.models import Sum,Count,IntegerField,Case, When,Value,F,ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth,ExtractMonth, ExtractYear,ExtractDay
from django.http import JsonResponse
from decimal import Decimal
import logging
from django.db import transaction
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import FornecedorForm, TipoUnitarioForm, EstiloForm,TipoForm,ServicoForm,laboratorioForm



logger = logging.getLogger('MyApp')


def get_aniversariantes_mes(request):
    cached_aniversariantes = cache.get('all_aniversariantes_mes')
    if cached_aniversariantes is None:
        today = timezone.now()
        current_month = today.month


        aniversariantes = CLIENTE.objects.annotate(
            birth_month=ExtractMonth('DATA_NASCIMENTO'),
            birth_day=ExtractDay('DATA_NASCIMENTO')
        ).filter(
            birth_month=current_month
        ).only('id', 'NOME', 'TELEFONE', 'DATA_NASCIMENTO', 'EMAIL').order_by('birth_day')

        cached_aniversariantes = [
            {
                'id': cliente.id,
                'NOME': cliente.NOME,
                'TELEFONE': cliente.TELEFONE.replace("(","").replace(")","").replace("-",""),
                'DATA_NASCIMENTO': cliente.DATA_NASCIMENTO,
                'EMAIL': cliente.EMAIL,
                'MENSAGEM_ANIVERSARIO':criar_mensagem_parabens(request,cliente.NOME),
            }
            for cliente in aniversariantes
        ]
        

        cache.set('all_aniversariantes_mes', cached_aniversariantes, timeout=129600)
    return cached_aniversariantes

@csrf_exempt
def fechar_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cliente_id = data.get('cliente_id')

        # Atualizar o cache removendo o cliente da lista de aniversariantes
        cached_aniversariantes = cache.get('all_aniversariantes_mes', [])
        updated_aniversariantes = [cliente for cliente in cached_aniversariantes if cliente['id'] != cliente_id]
        
        # Atualizar o cache com a nova lista de aniversariantes
        cache.set('all_aniversariantes_mes', updated_aniversariantes, timeout=129600)  # 30 dias = 2592000 segundos
        
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)

@login_required(login_url='/auth/logar/')  
def home(request):
    if request.user.is_authenticated:

        aniversariantes = get_aniversariantes_mes(request)
        alertas = AlertaEstoque.objects.filter(lido=False)
        for alerta in alertas:
            alerta.lido = True
            alerta.save()
        return render(request,'home.html',{'alertas': alertas,'aniversariantes':aniversariantes})
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
        CEP = request.POST.get('CEP')
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
        CEP=CEP,
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
            cliente.CEP = request.POST.get('CEP')
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
        return redirect('Core:clientes')

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
        if request.method == "GET":
            status = request.GET.get('status')
            data_inicio = request.GET.get('data_inicio')
            data_fim = request.GET.get('data_fim')

            if data_inicio and data_fim:
                Lista_os = Lista_os.filter(DATA_SOLICITACAO__range=[data_inicio, data_fim])

            if status:
                Lista_os = ORDEN.objects.order_by('-id').filter(STATUS=status)
            else:
                Lista_os = ORDEN.objects.order_by('-id').all()

            page = request.GET.get('page')

            Ordem_servicos = pagina.get_page(page)
            
            pagina = Paginator(Lista_os, 25)
            page = request.GET.get('page')
            Ordem_servicos = pagina.get_page(page)
            return render(request,'Os/Lista_Os.html',{'Ordem_servicos':Ordem_servicos,
                                                      'unidade':get_tenant(request).unidade,
                                                      'status': status,
                                                      'data_inicio': data_inicio,
                                                      'data_fim': data_fim,
                                                      })

@transaction.atomic
@login_required(login_url='/auth/logar/')
def Cadastrar_os(request,id_cliente):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id_cliente)
        servicos = SERVICO.objects.filter(ATIVO=True).all()
        laboratorios = LABORATORIO.objects.filter(ATIVO=True).all()
        produtos = Produto.objects.filter(quantidade__gt=0).order_by('-id')
        return render(request,'Os/cadastrar_os.html',{'cliente':cliente,'servicos':servicos,
                                                      'produtos':produtos,
                                                      'laboratorios':laboratorios,
                                                      })
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
                LAB = request.POST.get('lab')
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

                if ARMACAO != None:
                    realizar_saida(ARMACAO,1,f'Venda Por OS')
                else:
                    ARMACAO =''
                
                cadastrar_os = ORDEN(
                ANEXO= ANEXO,
                VENDEDOR = USUARIO.objects.get(id=VENDEDOR),
                CLIENTE = CLIENTE.objects.get(id=CLIENTE_POST),
                PREVISAO_ENTREGA= PREVISAO_ENTREGA,
                ASSINATURA =ASSINATURA,
                SERVICO= SERVICO.objects.get(id=SERVICO_POST),
                LABORATORIO= LABORATORIO.objects.get(id=LAB),
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
                                                       'unidade':get_tenant(request).unidade
                                                   })
    else:
        return render(request,'Os/Visualizar_os.htmll')
    
@transaction.atomic    
@login_required(login_url='/auth/logar/')
def Editar_os(request,id_os):
    if request.method == "GET":
        VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
        
        return render(request,'Os/Edita_os.html',{'VISUALIZAR_OS':VISUALIZAR_OS,
                                                  'unidade':get_tenant(request).unidade
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

            VISUALIZAR_OS.OD_ESF=OD_ESF
            VISUALIZAR_OS.OD_CIL=OD_CIL
            VISUALIZAR_OS.OD_EIXO=OD_EIXO
            VISUALIZAR_OS.OE_ESF=OE_ESF 
            VISUALIZAR_OS.OE_CIL=OE_CIL 
            VISUALIZAR_OS.OE_EIXO=OE_EIXO 
            VISUALIZAR_OS.AD=AD 
            VISUALIZAR_OS.DNP=DNP 
            VISUALIZAR_OS.P=P 
            VISUALIZAR_OS.DPA=DPA 
            VISUALIZAR_OS.DIAG=DIAG 
            VISUALIZAR_OS.V=V 
            VISUALIZAR_OS.H=H 
            VISUALIZAR_OS.ALT=ALT 
            VISUALIZAR_OS.ARM=ARM 
            VISUALIZAR_OS.MONTAGEM=MONTAGEM 
            VISUALIZAR_OS.LENTES=LENTES 
            VISUALIZAR_OS.ARMACAO=ARMACAO 
            VISUALIZAR_OS.OBSERVACAO=OBSERVACAO
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

def view_history(request, id):
    orden = get_object_or_404(ORDEN, id=id)
    history = orden.history.all()
    changes = []

    CHOICES_SITUACAO = (
        ('A', 'SOLICITADO'),
        ('E', 'ENTREGUE'),
        ('C', 'CANCELADO'),
        ('L', 'LABORATÓRIO'),
        ('J', 'LOJA')
    )

    CHOICES_PAGAMENTO = (
        ('A', 'PIX'),
        ('B', 'DINHEIRO'),
        ('C', 'DEBITO'),
        ('D', 'CREDITO'),
        ('E', 'CARNER'),
        ('F', 'PERMUTA'),
    )

    SITUACAO_DICT = dict(CHOICES_SITUACAO)
    PAGAMENTO_DICT = dict(CHOICES_PAGAMENTO)

    for record in history:
        if record.prev_record:
            diff = record.diff_against(record.prev_record)
            translated_changes = {}
            for change in diff.changes:
                old_value = change.old
                new_value = change.new
                if change.field == 'STATUS':
                    old_value = SITUACAO_DICT.get(change.old, change.old)
                    new_value = SITUACAO_DICT.get(change.new, change.new)
                elif change.field == 'FORMA_PAG':
                    old_value = PAGAMENTO_DICT.get(change.old, change.old)
                    new_value = PAGAMENTO_DICT.get(change.new, change.new)
                translated_changes[change.field] = {'old': old_value, 'new': new_value}
            changes.append({
                'history_date': record.history_date,
                'history_user': record.history_user,
                'changes': translated_changes,
            })

    return render(request, 'Os/view_history.html', {'orden': orden, 'changes': changes})


@login_required(login_url='/auth/logar/')
def Dashabord(request):
    solititado = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_30_days(),DATA_SOLICITACAO__lte=ultimo_dia_mes(),STATUS='A').order_by('id').all()
    laboratorio = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_30_days(),DATA_SOLICITACAO__lte=ultimo_dia_mes(),STATUS='L').order_by('id').all()
    loja = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_30_days(),DATA_SOLICITACAO__lte=ultimo_dia_mes(),STATUS='J').order_by('id').all()
    entregue = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_10_days(),DATA_SOLICITACAO__lte=get_today_data(),STATUS='E').order_by('id').all()

    return render(request,'dashabord/dashabord.html',{
        'solititado':solititado,
        'laboratorio':laboratorio,
        'loja':loja,
        'entregue':entregue,
    })

def update_card_status(request, card_id):
    if request.method == 'POST':
        try:
            # Capturar o objeto baseado no ID
            card = get_object_or_404(ORDEN, id=card_id)
            
            # Obter os dados enviados pelo HTMX
            data = json.loads(request.body)
            
            # Tentar obter o novo status
            new_status = data.get('status')

            # Atualizar o status no objeto e salvar
            card.STATUS = new_status
            card.save()

            # Atualiza o Kanban completo (parcial)
            solititado = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_30_days(),DATA_SOLICITACAO__lte=ultimo_dia_mes(),STATUS='A').order_by('id').all()
            laboratorio = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_30_days(),DATA_SOLICITACAO__lte=ultimo_dia_mes(),STATUS='L').order_by('id').all()
            loja = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_30_days(),DATA_SOLICITACAO__lte=ultimo_dia_mes(),STATUS='J').order_by('id').all()
            entregue = ORDEN.objects.filter(DATA_SOLICITACAO__gte=get_10_days(),DATA_SOLICITACAO__lte=get_today_data(),STATUS='E').order_by('id').all()

            # Renderiza o template parcial com o Kanban atualizado
            return render(request, 'parcial/kanban_partial.html', {
                'solititado': solititado,
                'laboratorio': laboratorio,
                'loja': loja,
                'entregue': entregue,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required(login_url='/auth/logar/')
def get_entrada_saida(self):
    # Buscar o último caixa fechado sem filtro de data
    ultimo_caixa_fechado = CAIXA.objects.filter(FECHADO=True, FORMA='B').order_by('DATA').last()
    
    # Se encontrar um caixa fechado, obtém o saldo final; caso contrário, saldo anterior é 0
    saldo_anterior = ultimo_caixa_fechado.SALDO_FINAL if ultimo_caixa_fechado else 0

    # Calcula entradas e saídas do dia corrente
    entradas = CAIXA.objects.filter(DATA__gte=primeiro_dia_mes(), DATA__lte=ultimo_dia_mes(), TIPO='E', FORMA='B', FECHADO=False).aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    saidas = CAIXA.objects.filter(DATA__gte=primeiro_dia_mes(), DATA__lte=ultimo_dia_mes(), TIPO='S', FORMA='B', FECHADO=False).aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    
    # Calcula o saldo atual
    saldo = round(entradas - saidas, 2)

    # Adiciona o saldo anterior ao saldo atual
    saldo_total_dinheiro = saldo + saldo_anterior

    # Calcula entradas totais (sem considerar apenas dinheiro)
    entradas_total = CAIXA.objects.filter(DATA__gte=primeiro_dia_mes(), DATA__lte=ultimo_dia_mes(), TIPO='E', FECHADO=False).aggregate(Sum('VALOR'))['VALOR__sum'] or 0

    return entradas, saidas, saldo_total_dinheiro, entradas_total

@login_required(login_url='/auth/logar/')
def Caixa(request):
    if request.method == "GET":
        try:
            dadoscaixa = dados_caixa()
            entradas,saida,saldo_total_dinheiro,entradas_total= get_entrada_saida(request)
            pagina = Paginator(dadoscaixa,15)
            page = request.GET.get('page')
            dados = pagina.get_page(page)
            return render(request,'Caixa/caixa.html',{'dados':dados,
                                                      'entrada':entradas,
                                                      'saida':saida,
                                                      'saldo':saldo_total_dinheiro,
                                                      'saldo_total':entradas_total})
        except Exception as msg:
            print(msg)
            logger.critical(msg)
    return render(request,'Caixa/caixa.html')

@login_required(login_url='/auth/logar/')
def fechar_caixa(request):
    # Filtrar o caixa do dia atual que ainda não foi fechado
    caixa = CAIXA.objects.filter(DATA__gte=primeiro_dia_mes(), DATA__lte=get_today_data(), FECHADO=False).order_by('-id')

    # Buscar o último caixa fechado, independentemente de datas
    ultimo_caixa_fechado = CAIXA.objects.filter(FECHADO=True, FORMA='B').order_by('DATA').last()

    # Se encontrar um caixa fechado, obtém o saldo final; caso contrário, saldo anterior é 0
    saldo_anterior = ultimo_caixa_fechado.SALDO_FINAL if ultimo_caixa_fechado else 0

    # Calcula entradas e saídas do dia corrente
    entradas = CAIXA.objects.filter(DATA__gte=primeiro_dia_mes(), DATA__lte=ultimo_dia_mes(), TIPO='E', FORMA='B', FECHADO=False).aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    saidas = CAIXA.objects.filter(DATA__gte=primeiro_dia_mes(), DATA__lte=ultimo_dia_mes(), TIPO='S', FORMA='B', FECHADO=False).aggregate(Sum('VALOR'))['VALOR__sum'] or 0
    
    # Calcula o saldo do dia
    saldo = round(entradas - saidas, 2)

    # Adiciona o saldo anterior ao saldo do dia para obter o saldo total
    saldo_total = round(saldo + saldo_anterior, 2)

    #print(saldo_total, 'saldo final ao fechar')

    # Atualiza o saldo final e fecha o caixa do dia
    for dado in caixa:
        dado.SALDO_FINAL = saldo_total
        dado.fechar_caixa()
        dado.save()

    messages.add_message(request, constants.SUCCESS, 'Caixa Fechado com sucesso')
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


@login_required(login_url='/auth/logar/')
def vendas_ultimos_12_meses(request):
    hoje = get_today_data()
    data_limite = hoje - timedelta(days=365)

    vendas = (
        ORDEN.objects
        .annotate(mes_venda=TruncMonth('DATA_SOLICITACAO')) 
        .values('mes_venda')
        .annotate(total_vendas=Sum('VALOR'))
        .filter(DATA_SOLICITACAO__gte=data_limite).exclude(STATUS='C')
        .order_by('mes_venda')
    )
    meses_portugues = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    # Formata a data para "Nome_do_Mês/Ano"
    data_vendas = [{
        'mes_venda': f"{meses_portugues[venda['mes_venda'].month]}/{venda['mes_venda'].year}",
        'total_vendas': venda['total_vendas']
    } for venda in vendas]

    return JsonResponse({'data': data_vendas})


@login_required(login_url='/auth/logar/')
def maiores_vendedores_30_dias(request):
    vendedores = ORDEN.objects.filter(DATA_SOLICITACAO__gte=primeiro_dia_mes(),DATA_SOLICITACAO__lte=ultimo_dia_mes()).exclude(STATUS='C') \
        .values('VENDEDOR__first_name') \
        .annotate(total_pedidos=Count('id')) \
        .annotate(total_valor_vendas=Sum('VALOR')) \
        .annotate(ticket_medio=ExpressionWrapper(
        F('total_valor_vendas') / F('total_pedidos'),
        output_field=DecimalField(max_digits=10, decimal_places=2)
    )) \
        .order_by('-total_pedidos')[:5]
  
    return JsonResponse({'maiores_vendedores_30_dias': list(vendedores)})


@login_required(login_url='/auth/logar/')
def maiores_vendedores_meses(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    vendedores = ORDEN.objects.filter(DATA_SOLICITACAO__gte=data_inicio,DATA_SOLICITACAO__lte=data_fim).exclude(STATUS='C') \
        .values('VENDEDOR__first_name') \
        .annotate(total_pedidos=Count('id')) \
        .annotate(total_valor_vendas=Sum('VALOR')) \
        .annotate(ticket_medio=ExpressionWrapper(
        F('total_valor_vendas') / F('total_pedidos'),
        output_field=DecimalField(max_digits=10, decimal_places=2)
    )) \
        .order_by('-total_pedidos')

    vendedores_formatados = []
    for vendedor in vendedores:
        vendedor_formatado = {
            'VENDEDOR__first_name': vendedor['VENDEDOR__first_name'],
            'total_pedidos': vendedor['total_pedidos'],
            'total_valor_vendas': format(Decimal(vendedor['total_valor_vendas'])),
            'ticket_medio': format(Decimal(vendedor['ticket_medio']))
        }
        vendedores_formatados.append(vendedor_formatado)

    return JsonResponse({'maiores_vendedores_30_dias':vendedores_formatados})

@login_required(login_url='/auth/logar/')
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

    # Mapeamento dos nomes dos meses em português
    meses_portugues = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

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
            'mes': meses_portugues[mes],
            'entrada': dados['entrada'],
            'saida': dados['saida'],
        }
        for (ano, mes), dados in dados_mensais.items()
    ]

    # Retorna os dados como JsonResponse
    return JsonResponse({'data': dados_formatados}, safe=False)

@login_required(login_url='/auth/logar/')
def caixa_mes_anterior(request):
    return render(request, 'Caixa/caixa_mes_anterior.html')

@login_required(login_url='/auth/logar/')
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
    

@login_required(login_url='/auth/logar/')
def obter_os_em_aberto(request):    
    
    vendas = (
        ORDEN.objects
        .annotate(mes_venda=TruncMonth('DATA_SOLICITACAO')) 
        .values('mes_venda')
        .annotate(total_vendas=Count('id'))
        .annotate(total_valor=Sum('VALOR'))  # Adicione essa linha para calcular o valor total das vendas
        .filter(DATA_SOLICITACAO__gte=primeiro_dia_mes(),DATA_SOLICITACAO__lte=ultimo_dia_mes())
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
def relatorio_mes_anterior(request):
    return render(request, 'Relatorio/relatorios_mes_html')

@login_required(login_url='/auth/logar/')
def dados_minhas_vendas(request):
    id_user = request.user
    vendedor = ORDEN.objects.filter(
        DATA_SOLICITACAO__gte=primeiro_dia_mes(),
        DATA_SOLICITACAO__lte=ultimo_dia_mes(),
        VENDEDOR=USUARIO.objects.get(id=id_user.id)
    ).exclude(STATUS='C') \
    .values('VENDEDOR__first_name') \
    .annotate(total_pedidos=Count('id')) \
    .annotate(total_valor_vendas=Sum('VALOR')) \
    .annotate(ticket_medio=ExpressionWrapper(
        F('total_valor_vendas') / F('total_pedidos'),
        output_field=DecimalField(max_digits=10, decimal_places=2)
    )) \
    .order_by('-total_pedidos')[:1]

    for item in vendedor:
        item['ticket_medio'] = format(item['ticket_medio'], '.2f')

    return JsonResponse({'minhas_vendas_mes': list(vendedor)})

@login_required(login_url='/auth/logar/')
def dados_clientes(request):
    total_clientes = CLIENTE.objects.exclude(STATUS='2').aggregate(total_clientes=Count('id'))['total_clientes']
    return JsonResponse({'total_clientes':total_clientes})

@login_required(login_url='/auth/logar/')
def receber(request):
    total_vendido = ORDEN.objects.filter(DATA_SOLICITACAO=get_today_data()).exclude(STATUS='C').aggregate(total=Sum('VALOR'))['total']

    if total_vendido is None:
        total_vendido = 0
    
    return JsonResponse({'total_vendido_hoje': total_vendido})

@login_required(login_url='/auth/logar/')
def minhas_vendas(request):
    return render(request,'minhas_vendas.html')

@login_required(login_url='/auth/logar/')
def estoque(request):
    quantidade = Produto.objects.aggregate(quantidade=Sum('quantidade'))

    if request.method == 'GET':
        fornecedores = Fornecedor.objects.all()
        unitarios = TipoUnitario.objects.all()
        tipo = Tipo.objects.all()
        estilo = Estilo.objects.all()
        Produtos = Produto.objects.all().order_by('-id')

        pagina = Paginator(Produtos, 25)

        page = request.GET.get('page')

        Produtos = pagina.get_page(page)

        codigo = request.GET.get('codigo')
        qtd = request.GET.get('qtd')
        fornecedor = request.GET.get('fornecedor')
        conf = request.GET.get('conf')
        ftipo = request.GET.get('ftipo')
        festilo = request.GET.get('festilo')

        if qtd or fornecedor or conf or ftipo or festilo or codigo:
            if qtd:
                Produtos = Produto.objects.filter(quantidade__gte=qtd,quantidade__lte=qtd).order_by('-id')

            if fornecedor:
                Produtos = Produto.objects.filter(fornecedor=fornecedor).order_by('-id')

            if ftipo:
                Produtos = Produto.objects.filter(Tipo=ftipo).order_by('-id')

            if conf:
                Produtos = Produto.objects.filter(conferido=True).order_by('-id')

            if codigo:
                Produtos = Produto.objects.filter(codigo=codigo).order_by('-id')

        return render(request,'Estoque/estoque.html',{'fornecedores':fornecedores,
                                                    'unitarios': unitarios,
                                                    'tipos':tipo,
                                                    'estilos':estilo,
                                                    'Produtos':Produtos,
                                                    'quantidade':quantidade}
                                                    )

@login_required(login_url='/auth/logar/')
def produto_estoque(request,id):
    produto = Produto.objects.get(pk=id)
    return render(request,'Estoque/entrada_produto.html',{'produto':produto})

@transaction.atomic
@login_required(login_url='/auth/logar/')
def realizar_entrada_view(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade'))
        realizar_entrada(produto_id=produto_id,quantidade=quantidade)
        messages.add_message(request, constants.SUCCESS, 'Entrada Registrada com sucesso')
        return redirect('/estoque')  
    else:
        messages.add_message(request, constants.ERROR, 'Nao Foi possivei Registrar a Entrada')
        return redirect('/estoque')
    
@transaction.atomic
@login_required(login_url='/auth/logar/')
def realizar_saida_view(request,id):
    produto = Produto.objects.get(pk=id)
    if request.method == 'GET':
        return render(request,'Estoque/saida_produto.html',{'produto':produto})
    else:
        quantidade = int(request.POST.get('quantidade'))
        observacao = request.POST.get('observacao')
        if realizar_saida(codigo=produto.codigo,quantidade=quantidade,observacao=observacao):
            messages.add_message(request, constants.SUCCESS, 'Saida Registrada com sucesso')
            return redirect('/estoque')
        else:
            messages.add_message(request, constants.ERROR, 'A quantidade de Saida e Maior que em Estoque')
            return redirect('/estoque')

@transaction.atomic
@login_required(login_url='/auth/logar/')
def editar_produto(request, id):
    edita_produto = Produto.objects.get(pk=id)
    if request.method == "GET":
        fornecedores = Fornecedor.objects.all()
        unitarios = TipoUnitario.objects.all()
        tipos = Tipo.objects.all()
        estilos = Estilo.objects.all()
        return render(request, 'Estoque/edita_estoque.html', {
            'fornecedores': fornecedores,
            'unitarios': unitarios,
            'tipos': tipos,
            'estilos': estilos,
            'edita_produto': edita_produto
        })
    elif request.method == "POST":
        edita_produto.chavenfe = request.POST.get('chavenfe')
        if len(edita_produto.chavenfe.strip()) == 0:
            edita_produto.chavenfe =None
        edita_produto.importado = True if request.POST.get('importado') == 'true' else False
        edita_produto.conferido = True if request.POST.get('conferido') == 'true' else False
        edita_produto.nome = request.POST.get('nome')
        edita_produto.fornecedor = Fornecedor.objects.get(pk=request.POST.get('fornecedor'))
        edita_produto.Tipo = Tipo.objects.get(pk=request.POST.get('tipo'))
        edita_produto.Estilo = Estilo.objects.get(pk=request.POST.get('estilo'))
        edita_produto.preco_unitario = Decimal(request.POST.get('preco_unitario').replace(".", "").replace(",", "."))
        edita_produto.preco_venda = Decimal(request.POST.get('preco_venda').replace(".", "").replace(",", "."))
        edita_produto.quantidade = int(request.POST.get('quantidade'))
        edita_produto.quantidade_minima = int(request.POST.get('quantidade_minima'))
        edita_produto.tipo_unitario = TipoUnitario.objects.get(pk=request.POST.get('tipo_unitario'))
        edita_produto.save()
        messages.add_message(request, constants.SUCCESS, 'Produto Editado com sucesso')
        return redirect('/estoque')

@login_required(login_url='/auth/logar/')
def movimentacao(request):
    movimento = MovimentoEstoque.objects.all().order_by('-id')

    pagina = Paginator(movimento, 25)

    page = request.GET.get('page')

    movimentacoes = pagina.get_page(page)

    return render(request,'Estoque/movimentacao_estoque.html',{'movimentacoes':movimentacoes})

@login_required(login_url='/auth/logar/')
def entradas_estoque(request):
    entradas = EntradaEstoque.objects.all().order_by('-id')

    pagina = Paginator(entradas, 25)

    page = request.GET.get('page')

    movimentacoes = pagina.get_page(page)

    return render(request,'Estoque/entradas_estoque.html',{'movimentacoes':movimentacoes})

@login_required(login_url='/auth/logar/')
def saidas_estoque(request):
    saidas = SaidaEstoque.objects.all().order_by('-id')

    pagina = Paginator(saidas, 25)

    page = request.GET.get('page')

    movimentacoes = pagina.get_page(page)

    return render(request,'Estoque/saidas_estoque.html',{'movimentacoes':movimentacoes})

def vendas(request):
    return render(request,'vendas.html')

class FornecedorListView(ListView):
    model = Fornecedor
    template_name = 'Estoque/fornecedor_list.html'

class FornecedorDetailView(DetailView):
    model = Fornecedor
    template_name = 'Estoque/fornecedor_detail.html'

class FornecedorCreateView(CreateView):
    with transaction.atomic():
        model = Fornecedor
        form_class = FornecedorForm
        template_name = 'Estoque/fornecedor_form.html'
        success_url = reverse_lazy('Core:fornecedor_list')

class FornecedorUpdateView(UpdateView):
    with transaction.atomic():
        model = Fornecedor
        form_class = FornecedorForm
        template_name = 'Estoque/fornecedor_form.html'
        success_url = reverse_lazy('Core:fornecedor_list')

class FornecedorDeleteView(DeleteView):
    model = Fornecedor
    template_name = 'Estoque/fornecedor_confirm_delete.html'
    success_url = reverse_lazy('Core:fornecedor_list')

class ServicoListView(ListView):
    model = SERVICO
    template_name = 'Os/os_list.html'

class ServicoCreateView(CreateView):
    with transaction.atomic():
        model = SERVICO
        form_class = ServicoForm
        template_name = 'Os/os_form.html'
        success_url = reverse_lazy('Core:os_list')

class TipoUnitarioListView(ListView):
    model = TipoUnitario
    template_name = 'Estoque/tipounitario_list.html'

class TipoUnitarioCreateView(CreateView):
    with transaction.atomic():
        model = TipoUnitario
        form_class = TipoUnitarioForm
        template_name = 'Estoque/tipounitario_form.html'
        success_url = reverse_lazy('Core:tiposund_list')

class TipoUnitarioDetailView(DetailView):
    model = TipoUnitario
    template_name = 'Estoque/tipounitario_detail.html'

class TipoUnitarioUpdateView(UpdateView):
    with transaction.atomic():
        model = TipoUnitario
        form_class = TipoUnitarioForm
        template_name = 'Estoque/tipounitario_form.html'
        success_url = reverse_lazy('Core:tiposund_list')

class TipoUnitarioDeleteView(DeleteView):
    model = TipoUnitario
    template_name = 'Estoque/tipounitario_confirm_delete.html'
    success_url = reverse_lazy('Core:tiposund_list')

class EstiloListView(ListView):
    model = Estilo
    template_name = 'Estoque/estilo_list.html'

class EstiloCreateView(CreateView):
    with transaction.atomic():
        model = Estilo
        form_class = EstiloForm
        template_name = 'Estoque/estilo_form.html'
        success_url = reverse_lazy('Core:estilos_list')

class EstiloDetailView(DetailView):
    model = Estilo
    template_name = 'Estoque/estilo_detail.html'

class EstiloUpdateView(UpdateView):
    with transaction.atomic():
        model = Estilo
        form_class = EstiloForm
        template_name = 'Estoque/estilo_form.html'
        success_url = reverse_lazy('Core:estilos_list')

class EstiloDeleteView(DeleteView):
    model = Estilo
    template_name = 'Estoque/estilo_confirm_delete.html'
    success_url = reverse_lazy('Core:estilos_list')

class TipoListView(ListView):
    model = Tipo
    template_name = 'Estoque/tipo_list.html'

class TipoCreateView(CreateView):
    with transaction.atomic():
        model = Tipo
        form_class = TipoForm
        template_name = 'Estoque/tipo_form.html'
        success_url = reverse_lazy('Core:tipos_list')

class TipoDetailView(DetailView):
    model = Tipo
    template_name = 'Estoque/tipo_detail.html'

class TipoUpdateView(UpdateView):
    with transaction.atomic():
        model = Tipo
        form_class = TipoForm
        template_name = 'Estoque/tipo_form.html'
        success_url = reverse_lazy('Core:tipos_list')

class TipoDeleteView(DeleteView):
    model = Tipo
    template_name = 'Estoque/tipo_confirm_delete.html'
    success_url = reverse_lazy('Core:tipos_list')


class LabListView(ListView):
    model = LABORATORIO
    template_name = 'Os/lab_list.html'

class LabCreateView(CreateView):
    with transaction.atomic():
        model = LABORATORIO
        form_class = laboratorioForm
        template_name = 'Os/os_form.html'
        success_url = reverse_lazy('Core:LabListView')


def historico_compras(request, cliente_id):
    cliente = get_object_or_404(CLIENTE, id=cliente_id)
    compras = ORDEN.objects.filter(CLIENTE=cliente).order_by('-DATA_SOLICITACAO')
    return render(request, 'Cliente/historico_compras.html', {'cliente': cliente, 'compras': compras})