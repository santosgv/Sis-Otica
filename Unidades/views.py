from django.shortcuts import redirect, render
from Autenticacao.models import ORDEN
from Unidades.models import CLIENTE_EXAME
from django.contrib.auth.decorators import login_required

def home(request):
    OS = ORDEN.objects.all()
    return render(request,'home.html',{'OS':OS})



@login_required(login_url='logar')
def cadastro_cliente(request):

    if request.method == "GET":
        print(request.method)
        return render(request, 'cadastro_cliente.html')
        
    elif request.method == "POST":
        exames = CLIENTE_EXAME.objects.all()
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
       

        ordem =ORDEN(NOME=NOME,LOGRADOURO=LOGRADOURO,NUMERO=NUMERO,BAIRRO=BAIRRO,CIDADE=CIDADE,TELEFONE=TELEFONE,CPF=CPF,DATA_NASCIMENTO=DATA_NASCIMENTO,EMAIL=EMAIL,EXAME=EXAME,FOTO=FOTO)
        ordem.save()
        print(request.method)
        return render(request,'cadastro_cliente.html',{'exames':exames})
