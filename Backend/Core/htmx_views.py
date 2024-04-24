from django.shortcuts import render
from Core.models import ORDEN,CLIENTE,Produto,Fornecedor,TipoUnitario
from decimal import Decimal



def search(request):
    search = request.GET.get('search')
    clientes = CLIENTE.objects.filter(NOME__icontains=search)
    ordens_de_servico_por_cliente = {}
    if clientes.exists():
        for cliente in clientes:
            ordens_de_servico = ORDEN.objects.filter(CLIENTE=cliente)
            ordens_de_servico_por_cliente[cliente] = ordens_de_servico

    return render(request,'parcial/os_parcial.html',{'Ordem_servicos':ordens_de_servico})


def search_cliente(request):
    search = request.GET.get('search_cliente')
    clientes = CLIENTE.objects.filter(NOME__icontains=search)
    return render(request,'parcial/cliente_parcial.html',{'clientes':clientes})


def all_estoque(request):
    return render(request,'parcial/produto_estoque.html')


def save_product(request):
    codigo = request.POST.get('Codigo')
    importado = request.POST.get('importado')
    nome = request.POST.get('nome')
    fornecedor = request.POST.get('fornecedor')
    preco_unitario = request.POST.get('preco_unitario').replace(".", "").replace(",", ".")
    preco =Decimal(preco_unitario)
    preco_venda = request.POST.get('preco_venda').replace(".", "").replace(",", ".")
    venda =Decimal(preco_venda)
    quantidade = request.POST.get('quantidade')
    quantidade_minima = request.POST.get('quantidade_minima')
    tipo_unitario = request.POST.get('tipo_unitario')

    if request.POST.get('importado') == 'true':
        importado =True
    else:
        importado =False

    prod = Produto.objects.create(
    importado = importado,
    codigo = codigo,
    nome = nome,
    fornecedor =Fornecedor.objects.get(id=fornecedor),
    preco_unitario =preco,
    preco_venda =venda,
    quantidade = int(quantidade),
    quantidade_minima = int(quantidade_minima),
    tipo_unitario = TipoUnitario.objects.get(id=tipo_unitario)
    )
    #prod.save()
    Produtos = Produto.objects.all()
    return render(request,'parcial/produto_estoque.html',{'Produtos':Produtos})
    