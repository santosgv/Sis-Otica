from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from Core.models import ORDEN,CLIENTE,SERVICO
from Unidades.models import UNIDADE
from Autenticacao.models import USUARIO
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



def home(request):
    OS = ORDEN.objects.all()
    return render(request,'home.html',{'OS':OS})

@login_required(login_url='logar')
def clientes(request):
    cliente_lista = CLIENTE.objects.all().order_by('NOME')

    pagina = Paginator(cliente_lista, 10)

    page = request.GET.get('page')

    clientes = pagina.get_page(page)

    return render(request,'Cliente/clientes.html',{'clientes':clientes})

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
        servicos = SERVICO.objects.all()
        context = {'cliente':cliente,
                    'servicos':servicos,
                                                }
        
        return render(request,'Os/cadastrar_os.html',context)
    else:
        try:
            ANEXO = request.POST.get('ANEXO')
            FILIAL = request.POST.get('FILIAL')
            VENDEDOR = request.POST.get('VENDEDOR')
            CLIENTE_POST = request.POST.get('CLIENTE')
            PREVISAO_ENTREGA = request.POST.get('PREVISAO_ENTREGA')
            SERVICO_POST =str(request.POST.get('SERVICO'))
            SUB_SERVICO_POST = request.POST.get('SUB_SERVICO')
            RECEITA = ('OD ESF: ',request.POST.get('OD_ESF'),
                        'OD CIL:',request.POST.get('OD_CIL'),
                        'OD EIXO: ',request.POST.get('OD_EIXO'),
                        'OE ESF: ',request.POST.get('OE_ESF'),
                        'OE CIL: ',request.POST.get('OE_CIL'),
                        'OE EIXO: ',request.POST.get('OE_EIXO'),
                        'AD: ',request.POST.get('AD'))
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
              SERVICO= SERVICO.objects.get(NOME=SERVICO_POST),
              SUB_SERVICO= SUB_SERVICO_POST,
              RECEITA= RECEITA,
              LENTES= LENTES,
              ARMACAO= ARMACAO,
              OBSERVACAO= OBSERVACAO,
              FORMA_PAG= FORMA_PAG,
              VALOR= VALOR,
              QUANTIDADE_PARCELA= QUANTIDADE_PARCELA,
              ENTRADA= ENTRADA     
            )
           
            cadastrar_os.save()
            messages.add_message(request, constants.SUCCESS, 'Dados Cadastrado com sucesso')
            return render(request,'Os/cadastrar_os.html')
        except Exception as msg:
            print(msg)
            messages.add_message(request, constants.ERROR, 'Erro interno ao salvar a OS')
            return render(request,'Os/cadastrar_os.html')

def Visualizar_os(request,id_os):
    if request.method == "GET":
        VISUALIZAR_OS = ORDEN.objects.get(id=id_os)
        return render(request,'Os/Visualizar_os.html',{'VISUALIZAR_OS':VISUALIZAR_OS,
                                                   })
    else:
        return render(request,'Os/Edita_os.html')

def Editar_os(request,id_os):
    if request.method == "GET":
        EDITAR_OS = ORDEN.objects.get(id=id_os)
        print(EDITAR_OS.ANEXO)
        return render(request,'Os/Editar_os.html',{'EDITAR_OS':EDITAR_OS,
                                                   })
    else:
        try:
            EDITAR_OS = ORDEN.objects.get(id=id_os)
            RECEITA = ('OD ESF: ',request.POST.get('OD_ESF'),
                      'OD CIL:',request.POST.get('OD_CIL'),
                      'OD EIXO: ',request.POST.get('OD_EIXO'),
                      'OE ESF: ',request.POST.get('OE_ESF'),
                      'OE CIL: ',request.POST.get('OE_CIL'),
                      'OE EIXO: ',request.POST.get('OE_EIXO'),
                      'AD: ',request.POST.get('AD'))
    
        
            EDITAR_OS.ANEXO = request.POST.get('ANEXO')
            EDITAR_OS.FILIAL = request.POST.get('FILIAL')
            EDITAR_OS.VENDEDOR = request.POST.get('VENDEDOR')
            EDITAR_OS.CLIENTE = request.POST.get('CLIENTE')
            EDITAR_OS.PREVISAO_ENTREGA = request.POST.get('PREVISAO_ENTREGA')
            EDITAR_OS.SERVICO = request.POST.get('SERVICO')
            EDITAR_OS.SUB_SERVICO = request.POST.get('SUB_SERVICO')
            EDITAR_OS.RECEITA = RECEITA
            EDITAR_OS.LENTES = request.POST.get('LENTES')
            EDITAR_OS.ARMACAO = request.POST.get('ARMACAO')
            EDITAR_OS.OBSERVACAO = request.POST.get('OBSERVACAO')
            EDITAR_OS.FORMA_PAG = request.POST.get('PAGAMENTO')
            EDITAR_OS.VALOR = request.POST.get('VALOR')
            EDITAR_OS.QUANTIDADE_PARCELA = request.POST.get('QUANTIDADE_PARCELA')
            EDITAR_OS.ENTRADA = request.POST.get('ENTRADA')
            EDITAR_OS.save()

            messages.add_message(request, constants.SUCCESS, 'Dados alterado com sucesso')
            return render(request,'Os/Edita_os.html',{'EDITAR_OS':EDITAR_OS})
        except Exception as msg:
            print(msg)
            return render(request,'Os/Editar_os.html')        
        