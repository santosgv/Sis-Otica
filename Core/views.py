from django.shortcuts import redirect, render




def cadastra_cliente(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastra_cliente.html')

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
        FOTO = request.POST.get('FOTO')
