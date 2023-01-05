from django.shortcuts import redirect, render
from Autenticacao.models import ORDEN,CLIENTE
from Unidades.models import CLIENTE_EXAME
from django.contrib.auth.decorators import login_required


def home(request):
    OS = ORDEN.objects.all()
    return render(request,'home.html',{'OS':OS})


def clientes(request):
    clientes = CLIENTE.objects.all()
    return render(request,'clientes.html',{'clientes':clientes})

@login_required(login_url='logar')
def cadastro_cliente(request):

    if request.method == "GET":
        exames = CLIENTE_EXAME.objects.all()
        print(exames)
        return render(request, 'cadastro_cliente.html',{'exames':exames})
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
        EXAME = request.POST.get('EXAME')
        FOTO =  request.POST.get('FOTO')       
       
        cliente =CLIENTE(NOME=NOME,
        LOGRADOURO=LOGRADOURO,
        NUMERO=NUMERO,
        BAIRRO=BAIRRO,
        CIDADE=CIDADE,
        TELEFONE=TELEFONE,
        CPF=CPF,
        DATA_NASCIMENTO=DATA_NASCIMENTO,
        EMAIL=EMAIL,
        EXAME=CLIENTE_EXAME.objects.get(id=EXAME)
        ,FOTO=FOTO)
        cliente.save()

        return render(request,'cadastro_cliente.html')
