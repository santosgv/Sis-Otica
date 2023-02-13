from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from Core.models import ORDEN,CLIENTE
from Unidades.models import UNIDADE
from Autenticacao.models import USUARIO
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime

from reportlab.pdfgen import canvas
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter

def home(request):
    OS = ORDEN.objects.all()
    return render(request,'home.html',{'OS':OS})

@login_required(login_url='logar')
def clientes(request):
    cliente_lista = CLIENTE.objects.all().order_by('NOME').order_by('-DATA_CADASTRO').values()

    pagina = Paginator(cliente_lista, 10)

    page = request.GET.get('page')

    clientes = pagina.get_page(page)
    
    return render(request,'Cliente/clientes.html',{'clientes':clientes,
                                                    })

@login_required(login_url='logar')
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

@login_required(login_url='logar')
def Cliente(request,id):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id)
        return render(request,'Cliente/cliente.html',{'cliente':cliente})

@login_required(login_url='logar')
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

@login_required(login_url='logar')
def excluir_cliente(request,id):
    excluir = CLIENTE.objects.get(id=id)
    excluir.delete()
    return redirect('/clientes')

@login_required(login_url='logar')
def Lista_Os(request):

    Lista_os = ORDEN.objects.all().order_by('id')

    pagina = Paginator(Lista_os, 10)

    page = request.GET.get('page')

    Ordem_servicos = pagina.get_page(page)

    return render(request,'Os/Lista_Os.html',{'Ordem_servicos':Ordem_servicos})

def Cadastrar_os(request,id_os):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id_os)
        return render(request,'Os/cadastrar_os.html',{'cliente':cliente})
    else:
        try:
            ANEXO = request.FILES['ANEXO']
            FILIAL = request.POST.get('FILIAL')
            VENDEDOR = request.POST.get('VENDEDOR')
            CLIENTE_POST = request.POST.get('CLIENTE')
            PREVISAO_ENTREGA = request.POST.get('PREVISAO_ENTREGA')
            SERVICO_POST =str(request.POST.get('SERVICO'))
            SUB_SERVICO_POST = request.POST.get('SUB_SERVICO')
            OD_ESF = request.POST.get('OD_ESF')
            OD_CIL = request.POST.get('OD_CIL')
            OD_EIXO = request.POST.get('OD_EIXO')
            OE_ESF = request.POST.get('OE_ESF')
            OE_CIL = request.POST.get('OE_CIL')
            OE_EIXO = request.POST.get('OE_EIXO')
            AD = request.POST.get('AD')
            LENTES = request.POST.get('LENTES')
            ARMACAO = request.POST.get('ARMACAO')
            OBSERVACAO = request.POST.get('OBSERVACAO')
            FORMA_PAG = request.POST.get('PAGAMENTO')
            VALOR = request.POST.get('VALOR')
            QUANTIDADE_PARCELA = request.POST.get('QUANTIDADE_PARCELA')
            ENTRADA = request.POST.get('ENTRADA')
           
            cadastrar_os = ORDEN(
            ANEXO= ANEXO,
            FILIAL= UNIDADE.objects.get(NOME=FILIAL),
            VENDEDOR = USUARIO.objects.get(id=VENDEDOR),
            CLIENTE = CLIENTE.objects.get(id=CLIENTE_POST),
            PREVISAO_ENTREGA= PREVISAO_ENTREGA,
            SERVICO= SERVICO_POST,
            SUB_SERVICO= SUB_SERVICO_POST,
            OD_ESF= OD_ESF,
            OD_CIL = OD_CIL,
            OD_EIXO = OD_EIXO,
            OE_ESF = OE_ESF,
            OE_CIL = OE_CIL,
            OE_EIXO = OE_EIXO,
            AD = AD,
            LENTES= LENTES,
            ARMACAO= ARMACAO,
            OBSERVACAO= OBSERVACAO,
            FORMA_PAG= FORMA_PAG,
            VALOR= VALOR,
            QUANTIDADE_PARCELA= QUANTIDADE_PARCELA,
            ENTRADA= ENTRADA     
          )
            
            cadastrar_os.save()
        
            cliente = CLIENTE.objects.get(id=id_os)
            messages.add_message(request, constants.SUCCESS, 'Dados Cadastrado com sucesso')
            return render(request,'OS/cadastro_cliente.html',{'cliente':cliente})  
        except Exception as msg:
            print(msg)
            cliente = CLIENTE.objects.get(id=id_os)
            messages.add_message(request, constants.ERROR, 'Erro interno ao salvar a OS')
            return render(request,'Os/cadastrar_os.html',{'cliente':cliente}) 

def Visualizar_os(request,id_os):
    if request.method == "GET":
        VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
        return render(request,'Os/Visualizar_os.html',{'VISUALIZAR_OS':VISUALIZAR_OS,
                                                   })
    else:
        return render(request,'Os/Visualizar_os.htmll')

def Encerrar_os(request,id_os):
    if request.method == "GET":
        try:
            Encerrar_OS = ORDEN.objects.get(id=id_os)
            Encerrar_OS.STATUS = "E"
            Encerrar_OS.DARA_ENCERRAMENTO =datetime.now()
            Encerrar_OS.save()
            messages.add_message(request, constants.SUCCESS, 'O.s Encerrada com sucesso')
            return redirect('/Lista_Os')  
        except Exception as msg:
            print(msg)
            return redirect('/Lista_Os')   

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
        
def Imprimir_os(request,id_os):
    try:
        PRINT_OS =ORDEN.objects.get(id=id_os)
        
        buffer = io.BytesIO()
        PDF = canvas.Canvas(buffer,pagesize=letter)
        PDF.setFont('Helvetica', 15)

        PDF.drawString(30,750,'VENDEDOR : ' + str(PRINT_OS.VENDEDOR.first_name))
        PDF.drawString(30,725,'CLIENTE : '+ str(PRINT_OS.CLIENTE))
        PDF.drawString(300,750,'O.S : ' +str(PRINT_OS.id))
        PDF.drawString(400,750,'FILIAL : ' +str(PRINT_OS.FILIAL))
        
        PDF.drawString(300,725,'PREVISAO ENTREGA :')
        PDF.drawString(500,725,str(PRINT_OS.PREVISAO_ENTREGA))
        PDF.line(30,715,580,715)
        PDF.drawString(250,700,'SERVIÇOS')
        PDF.drawString(30,650,'SERVIÇO : ' + str(PRINT_OS.SERVICO))
        PDF.drawString(300,650,'SUB SERVIÇO : ' + str(PRINT_OS.SUB_SERVICO))
        PDF.drawString(250,600,'RECEITA')
        PDF.drawString(30,550,'LENTES : '+ str(PRINT_OS.LENTES))
        PDF.drawString(300,550,'ARMACAO : '+ str(PRINT_OS.ARMACAO))
        PDF.drawString(250,500,'OBSERVAÇÂO')
        PDF.drawString(30,450,str(PRINT_OS.OBSERVACAO))
        

        PDF.drawString(30,30,'ASSINATURA DO CLIENTE: ')
        PDF.line(250,30,580,30)
        PDF.showPage()
        PDF.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='OS.pdf')
    except Exception as msg:
        print(msg)
        return redirect('/Lista_Os') 