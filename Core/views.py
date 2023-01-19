from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render,get_object_or_404
from Core.models import ORDEN,CLIENTE
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

    return render(request,'clientes.html',{'clientes':clientes})

@login_required(login_url='logar')
def cadastro_cliente(request):

    if request.method == "GET":
        return render(request, 'cadastro_cliente.html')
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
        return render(request,'cliente.html',{'cliente':cliente})

@login_required(login_url='logar')
def Edita_cliente(request,id):
    if request.method == "GET":
        cliente = CLIENTE.objects.get(id=id)
        print('GET')
        return render(request,'edita_cliente.html',{'cliente':cliente})
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
    return render(request,'edita_cliente.html',{'cliente':cliente})

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

    return render(request,'Lista_Os.html',{'Ordem_servicos':Ordem_servicos})


def Cadastrar_os(request,id_cliente):
    cliente = CLIENTE.objects.get(id=id_cliente)

    return render(request,'cadastrar_os.html',{'cliente':cliente})
