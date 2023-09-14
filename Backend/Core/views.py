import os
from django.contrib import messages
from datetime import datetime
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from Core.models import ORDEN,CLIENTE
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


def home(request):
    if request.user.is_authenticated:
        return render(request,'home.html',)
    else:
        return render(request,'home.html')


@login_required(login_url='/auth/logar/')
def clientes(request):
    if request.user.is_superuser ==True:
        cliente_lista = CLIENTE.objects.all().order_by('NOME').order_by('-DATA_CADASTRO')
        pagina = Paginator(cliente_lista, 10)

        page = request.GET.get('page')

        clientes = pagina.get_page(page)
        
        return render(request,'Cliente/clientes.html',{'clientes':clientes,
                                                        })
    else:
        cliente_lista = CLIENTE.objects.all().order_by('NOME').order_by('-DATA_CADASTRO').values()

        pagina = Paginator(cliente_lista, 10)

        page = request.GET.get('page')

        clientes = pagina.get_page(page)
        
        return render(request,'Cliente/clientes.html',{'clientes':clientes,
                                                        })

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

@login_required(login_url='/auth/logar/')
def Edita_cliente(request,id):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id)
        return render(request,'Cliente/edita_cliente.html',{'cliente':cliente})
    else:
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
    return render(request,'Cliente/edita_cliente.html',{'cliente':cliente})

@login_required(login_url='/auth/logar/')
def excluir_cliente(request,id):
    excluir = CLIENTE.objects.get(id=id)
    excluir.delete()
    return redirect('/clientes')

@login_required(login_url='/auth/logar/')
def Lista_Os(request):
    if request.user.is_superuser ==True:
        Lista_os = ORDEN.objects.all().order_by('-id')

        pagina = Paginator(Lista_os, 10)

        page = request.GET.get('page')

        Ordem_servicos = pagina.get_page(page)

        return render(request,'Os/Lista_Os.html',{'Ordem_servicos':Ordem_servicos})
    else:
        Lista_os = ORDEN.objects.all().order_by('id')

        pagina = Paginator(Lista_os, 10)

        page = request.GET.get('page')

        Ordem_servicos = pagina.get_page(page)

        return render(request,'Os/Lista_Os.html',{'Ordem_servicos':Ordem_servicos})

@login_required(login_url='/auth/logar/')
def Cadastrar_os(request,id_cliente):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id_cliente)
        return render(request,'Os/cadastrar_os.html',{'cliente':cliente})
    else:
        try:
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
            SERVICO_POST =str(request.POST.get('SERVICO'))
            SUB_SERVICO_POST = request.POST.get('SUB_SERVICO')
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
            VALOR = request.POST.get('VALOR')
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
            SERVICO= SERVICO_POST,
            SUB_SERVICO= SUB_SERVICO_POST,
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
            VALOR= VALOR,
            QUANTIDADE_PARCELA= QUANTIDADE_PARCELA,
            ENTRADA= ENTRADA )



            cadastrar_os.save()

            messages.add_message(request, constants.SUCCESS, 'O.S Cadastrado com sucesso')
            return redirect('/Lista_Os')  
        except Exception as msg:
            print(msg)
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
    
@login_required(login_url='/auth/logar/')
def Editar_os(request,id_os):
    if request.method == "GET":
        VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
        
        return render(request,'Os/Edita_os.html',{'VISUALIZAR_OS':VISUALIZAR_OS,
                                                   })
    else:

        FORMA_PAG = request.POST.get('PAGAMENTO')
        VALOR = request.POST.get('VALOR')
        QUANTIDADE_PARCELA = request.POST.get('QUANTIDADE_PARCELA')

        if request.POST.get('ENTRADA') == '':
            ENTRADA =0
        else:
            ENTRADA = request.POST.get('ENTRADA')
        
        VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
        VISUALIZAR_OS.FORMA_PAG=FORMA_PAG
        VISUALIZAR_OS.VALOR=VALOR
        VISUALIZAR_OS.QUANTIDADE_PARCELA=QUANTIDADE_PARCELA
        VISUALIZAR_OS.ENTRADA=ENTRADA
        VISUALIZAR_OS.save()
        
        messages.add_message(request, constants.SUCCESS, 'O.S Editada com sucesso')
        return redirect('/Lista_Os')  

@login_required(login_url='/auth/logar/')
def Encerrar_os(request,id_os):
    if request.method == "GET":
        try:
            Encerrar_OS = ORDEN.objects.get(id=id_os)
            Encerrar_OS.STATUS = "E"
            Encerrar_OS.DARA_ENCERRAMENTO =now()
            Encerrar_OS.save()
            messages.add_message(request, constants.SUCCESS, 'O.s Encerrada com sucesso')
            return redirect('/Lista_Os')  
        except Exception as msg:
            print(msg)
            return redirect('/Lista_Os')   

@login_required(login_url='/auth/logar/')
def Cancelar_os(request,id_os):
    if request.method == "GET":
        try:
            CANCELAR_OS = ORDEN.objects.get(id=id_os)
            CANCELAR_OS.STATUS ="C"
            CANCELAR_OS.save()
            messages.add_message(request, constants.SUCCESS, 'O.s Foi Cancelada com sucesso')
            return redirect('/Lista_Os')  
        except Exception as msg:
            print(msg)
            return redirect('/Lista_Os')
        
@login_required(login_url='/auth/logar/')
def Laboratorio_os(request,id_os):
    if request.method == "GET":
        try:
            Laboratorio_os = ORDEN.objects.get(id=id_os)
            Laboratorio_os.STATUS ="L"
            Laboratorio_os.save()
            messages.add_message(request, constants.SUCCESS, 'O.s Foi Movido para o Laboratorio com sucesso')
            return redirect('/Lista_Os')  
        except Exception as msg:
            print(msg)
            return redirect('/Lista_Os')  

@login_required(login_url='/auth/logar/')
def Loja_os(request,id_os):
    if request.method == "GET":
        try:
            Loja_os = ORDEN.objects.get(id=id_os)
            Loja_os.STATUS ="J"
            Loja_os.save()
            messages.add_message(request, constants.SUCCESS, 'O.s Foi Movido para a Loja com sucesso')
            return redirect('/Lista_Os')  
        except Exception as msg:
            print(msg)
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
        PDF.drawString(88,724,str(PRINT_OS.CLIENTE))
        PDF.drawString(385,724,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d-%m-%Y')))
        PDF.drawString(88,665,str(PRINT_OS.SERVICO))
        PDF.drawString(385,665,str(PRINT_OS.SUB_SERVICO))
        PDF.drawString(88,637,str(PRINT_OS.LENTES))
        PDF.drawString(88,620,str(PRINT_OS.ARMACAO))
        PDF.drawString(109,592,str(PRINT_OS.OBSERVACAO))
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
        PDF.drawString(88,402,str(PRINT_OS.CLIENTE))
        PDF.drawString(385,402,str(PRINT_OS.PREVISAO_ENTREGA.strftime('%d-%m-%Y')))
        PDF.drawString(88,361,str(PRINT_OS.SERVICO))
        PDF.drawString(338,361,str(PRINT_OS.SUB_SERVICO))
        PDF.drawString(88,312,str(PRINT_OS.OD_ESF))
        PDF.drawString(88,282,str(PRINT_OS.OE_ESF))
        PDF.drawString(301,312,str(PRINT_OS.OD_CIL))
        PDF.drawString(301,282,str(PRINT_OS.OE_CIL))
        PDF.drawString(472,312,str(PRINT_OS.OD_EIXO))
        PDF.drawString(472,282,str(PRINT_OS.OE_EIXO))
        PDF.drawString(64,248,str(PRINT_OS.AD))
        PDF.drawString(78,215,str(PRINT_OS.LENTES))
        PDF.drawString(78,197,str(PRINT_OS.ARMACAO))
        PDF.drawString(109,178,str(PRINT_OS.OBSERVACAO))

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
        return FileResponse(buffer, as_attachment=True, filename='OS.pdf')
    except Exception as msg:
        print(msg)
        return redirect('/Lista_Os')

     
@login_required(login_url='/auth/logar/')
def Dashabord(request):
    date_now  = datetime.datetime.now().date()
    thirty_days_ago = date_now - datetime.timedelta(days=30)
    if request.user.is_superuser ==True:
        Lista_os = ORDEN.objects.all().filter(DATA_SOLICITACAO__gte=thirty_days_ago,DATA_SOLICITACAO__lte=date_now).order_by('id')
        
        pagina = Paginator(Lista_os, 10)

        page = request.GET.get('page')
        
        kankan_servicos = pagina.get_page(page)

        return render(request,'dashabord/dashabord.html',{'kankan_servicos':kankan_servicos})
    else:
        pega_filial =USUARIO.objects.get(id=request.user.id)
        Lista_os = ORDEN.objects.all().filter(DATA_SOLICITACAO__gte=thirty_days_ago,DATA_SOLICITACAO__lte=date_now).order_by('id')
        pagina = Paginator(Lista_os, 10)

        page = request.GET.get('page')

        kankan_servicos = pagina.get_page(page)
    return render(request,'dashabord/dashabord.html',{'kankan_servicos':kankan_servicos})
    