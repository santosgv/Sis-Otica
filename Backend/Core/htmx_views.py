from django.shortcuts import render,HttpResponse
from Core.models import ORDEN,CLIENTE



def search(request):
    search = request.GET.get('search')
    clientes = CLIENTE.objects.filter(NOME__icontains=search)
    ordens_de_servico_por_cliente = {}
    if clientes.exists():
        for cliente in clientes:
            ordens_de_servico = ORDEN.objects.filter(CLIENTE=cliente)
            ordens_de_servico_por_cliente[cliente] = ordens_de_servico

    return render(request,'parcial/os_parcial.html',{'Ordem_servicos':ordens_de_servico})
