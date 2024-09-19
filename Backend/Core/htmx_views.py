from django.shortcuts import render
from Core.models import ORDEN,CLIENTE,Produto,Fornecedor,TipoUnitario,Tipo,Estilo
from decimal import Decimal
from django.core.paginator import Paginator
from .views import realizar_entrada
from django.db.models.functions import Replace
from django.db.models import Value


def search(request):
    search = request.GET.get('search')
    clientes = CLIENTE.objects.filter(NOME__icontains=search)
    ordens_de_servico_por_cliente = {}
    if clientes.exists():
        for cliente in clientes:
            ordens_de_servico = ORDEN.objects.filter(CLIENTE=cliente)
            ordens_de_servico_por_cliente[cliente] = ordens_de_servico

    return render(request,'parcial/os_parcial.html',{'Ordem_servicos':ordens_de_servico})

def search_products(request):
    search_term = request.GET.get('search_products', '').replace('-', '')
    produtos = Produto.objects.annotate(
        codigo_sem_hifen=Replace('codigo', Value('-'), Value(''))
    ).filter(
        codigo_sem_hifen__icontains=search_term,
        quantidade__gt=0
    )
    return render(request, 'parcial/select_options.html', {'produtos': produtos})

def search_caixa(request):
    search_term = request.GET.get('search_os')
    orden = ORDEN.objects.filter(id__icontains=search_term).exclude(STATUS='C').exclude(STATUS='E').all()
    return render(request, 'parcial/select_os.html', {'OsS': orden})

def search_cliente(request):
    search = request.GET.get('search_cliente')
    clientes = CLIENTE.objects.filter(NOME__icontains=search)
    return render(request,'parcial/cliente_parcial.html',{'clientes':clientes})

def all_estoque(request):
    return render(request,'parcial/produto_estoque.html')

def save_product(request):
    chavenfe = request.POST.get('chavenfe')
    importado = request.POST.get('importado')
    conferido = request.POST.get('conferido')
    nome = request.POST.get('nome')
    fornecedor = request.POST.get('fornecedor')
    tipo = request.POST.get('tipo')
    estilo = request.POST.get('estilo')
    preco_unitario = request.POST.get('preco_unitario').replace(".", "").replace(",", ".")
    preco =Decimal(preco_unitario)
    preco_venda = request.POST.get('preco_venda').replace(".", "").replace(",", ".")
    venda =Decimal(preco_venda)
    quantidade = request.POST.get('quantidade')
    quantidade_minima = request.POST.get('quantidade_minima')
    tipo_unitario = request.POST.get('tipo_unitario')

    if request.POST.get('importado') == 'true':
        importado = True
    else:
        importado = False

    if request.POST.get('conferido') == 'true':
        conferido = True
    else:
        conferido = False

    if len(chavenfe.strip()) == 0:
        chavenfe =None
  
    try:
        prod = Produto.objects.create(
        importado = importado,
        conferido =conferido,
        chavenfe= chavenfe,
        nome = nome,
        fornecedor =Fornecedor.objects.get(id=fornecedor),
        Tipo =Tipo.objects.get(id=tipo),
        Estilo =Estilo.objects.get(id=estilo),
        preco_unitario =preco,
        preco_venda =venda,
        quantidade = int(quantidade),
        quantidade_minima = int(quantidade_minima),
        tipo_unitario = TipoUnitario.objects.get(id=tipo_unitario)
        )
        realizar_entrada(produto_id=prod.id,quantidade=int(quantidade))
        prod.save()
    except Exception as Msg:
        print(Msg)
    Produtos = Produto.objects.all().order_by('-id')
    return render(request,'parcial/produto_estoque.html',{'Produtos':Produtos})
    