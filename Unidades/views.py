from django.shortcuts import redirect, render
from Autenticacao.models import ORDEN

def home(request):
    OS = ORDEN.objects.all()
    return render(request,'home.html',{'OS':OS})

def cadastro_cliente(request):
    if request.method == "GET":
        return render(request, 'cadastro_cliente.html')
    elif request.method == "POST":
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
        
        return render(request,'cadastro_cliente.html')