from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import USUARIO, Ativacao,Desconto,Comissao
from django.contrib import auth
from django.conf import settings
from datetime import date
from .utils import email_html,calcular_inss,calcular_irrf,generate_pdf
from hashlib import sha256
from django.core.mail import EmailMultiAlternatives
#from django.template.loader import render_to_string
#from django.utils.html import strip_tags
import os
import logging
from Core.utils import primeiro_dia_mes,ultimo_dia_mes
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ColaboradorForm, DescontoForm, ComissaoForm

logger = logging.getLogger('MyApp')

def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
        
    elif request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        funcao = request.POST.get('funcao')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm-password')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/auth/cadastro')

        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro')
        
        user = USUARIO.objects.filter(username=username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
            return redirect('/auth/cadastro')
        
        try:
            path_template = os.path.join(settings.BASE_DIR, 'Autenticacao/templates/emails/cadastro_confirmado.html')
            base_url = request.build_absolute_uri('/')
            user = USUARIO.objects.create_user(username=username,
                                            first_name=first_name,
                                            DATA_NASCIMENTO=data_nascimento,
                                            CPF=cpf,
                                            FUNCAO= funcao,
                                            email = email,
                                            password=senha)
            user.save()
            token =sha256(f"{username}{email}".encode()).hexdigest()

            ativacao =Ativacao(token=token, user=user)
            ativacao.save()
            link_ativacao=f"{settings.ALLOWED_HOSTS[0]}/auth/ativar_conta/{token}" 
            email_html(path_template, 'Cadastro confirmado', [email,], username=username, base_url=base_url ,link_ativacao=link_ativacao)
            #link_ativacao=f"{settings.ALLOWED_HOSTS[0]}/auth/auth/ativar_conta/{token}" #ESSE METODO E DO ENVIO DO PROPRIO DJANGO
            #html_content=render_to_string('emails/cadastro_confirmado.html',{'username':username,'link_ativacao':link_ativacao})
            #text_content = strip_tags(html_content)
            #email = EmailMultiAlternatives('Cadastro confirmado',text_content,settings.EMAIL_HOST_USER,[email,])
            #email.attach_alternative(html_content,'text/html')
            #email.send()
            messages.add_message(request, constants.SUCCESS, 'Foi Enviado Para seu email o Link de ativaçao da sua conta')
            return redirect('/auth/logar')
        except Exception as msg:
            logger.critical(msg)
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')

def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')

        usuario = auth.authenticate(username=username, password=senha)


        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return redirect('/')

def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/logar')
    user = USUARIO.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/logar')

def alterar_conta(request):
    if request.method == "GET":
        username = request.user.username
        first_name = request.user.first_name
        cpf = request.user.CPF
       # data_nascimento = request.user.DATA_NASCIMENTO
        email = request.user.email

        return render(request,'alterar_conta.html',{
                                                'username':username,
                                                'first_name':first_name,
                                                'cpf': cpf,
                                              #  'data_nascimento':data_nascimento,
                                                'email':email
                                                    })
    else:
        
        usuario = request.user
        first_name = request.POST.get('first_name')
        cpf = request.POST.get('cpf')
        #data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')


        if len(first_name.strip()) == 0  or len(cpf.strip()) == 0 or len(email.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/alterar_conta')
        
        user = USUARIO.objects.filter(username=request.user).exclude(id=request.user.id)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usário com esse username')
            return redirect('/auth/alterar_conta')

        usuario = request.user
        usuario.first_name = first_name
      #  usuario.DATA_NASCIMENTO = data_nascimento
        usuario.CPF = cpf
        usuario.email = email
        usuario.save()
        auth.logout(request)
    messages.add_message(request, constants.SUCCESS, 'Dados de Usuario Alterado com Sucesso, Faça novamente o Login para Validar')
    return redirect('/auth/logar')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')

@login_required(login_url='/auth/logar/')
def listar_folha_pagamento(request):
    if request.user.FUNCAO == 'G':
        colaboradores = USUARIO.objects.filter(is_active=True).all()
    else:
        colaboradores = USUARIO.objects.filter(pk=request.user.pk)

    # Pre-fetch related objects to reduce the number of queries
    colaboradores = colaboradores.prefetch_related(
        'desconto_set', 
        'comissao_set'
    )

    folha_pagamento = []



    for colaborador in colaboradores:
        salario_bruto = colaborador.salario_bruto

        desconto_inss = calcular_inss(salario_bruto)

        # Calculate total discounts
        total_descontos = sum(
            [salario_bruto * (desconto.percentual / 100) for desconto in colaborador.desconto_set.all()]
        )

        # Calculate total commissions
        comissoes = colaborador.comissao_set.filter(
            data_referencia__gte=primeiro_dia_mes(), 
            data_referencia__lte=ultimo_dia_mes()
        )

        total_comissao = sum([comissao.calcular_comissao() for comissao in comissoes])
        

        # Calculate total extra hours
        total_horas = sum([comissao.calcula_horas_extras() for comissao in comissoes])

        # Calcular salário líquido parcial (antes do IRRF)
        salario_liquido_parcial = salario_bruto - total_descontos - desconto_inss + total_comissao + total_horas

        # Calcular desconto do IRRF baseado no salário líquido parcial
        desconto_irrf = calcular_irrf(salario_liquido_parcial)

        # Atualizar total de descontos
        total_descontos += desconto_inss + desconto_irrf

        # Calcular salário líquido final
        salario_liquido = salario_bruto - total_descontos + total_comissao + total_horas
        
        folha_pagamento.append({
            'colaborador': colaborador,
            'salario_bruto': round(salario_bruto, 2),
            'total_descontos': round(total_descontos, 2),
            'total_comissao': round(total_comissao, 2),
            'total_horas': round(total_horas, 2),
            'salario_liquido': round(salario_liquido, 2),
            'desconto_inss':desconto_inss,
            'desconto_irrf':desconto_irrf,
            'comissoes': comissoes,
            'descontos': colaborador.desconto_set.all(),
        })

    return render(request, 'controle_pagamento/listar_folha_pagamento.html', {
        'folha_pagamento': folha_pagamento,
        'mes_atual': primeiro_dia_mes(),
        'ano_atual': ultimo_dia_mes(),
    })

class ColaboradorListView(ListView):
    model = USUARIO
    template_name = 'controle_pagamento/colaborador_list.html'

class ColaboradorDetailView(DetailView):
    model = USUARIO
    template_name = 'controle_pagamento/colaborador_detail.html'

class ColaboradorUpdateView(UpdateView):
    model = USUARIO
    form_class = ColaboradorForm
    template_name = 'controle_pagamento/colaborador_form.html'
    success_url = reverse_lazy('colaborador_list')

class DescontoListView(ListView):
    model = Desconto
    template_name = 'controle_pagamento/desconto_list.html'

class DescontoDetailView(DetailView):
    model = Desconto
    template_name = 'controle_pagamento/desconto_detail.html'

class DescontoCreateView(CreateView):
    model = Desconto
    form_class = DescontoForm
    template_name = 'controle_pagamento/desconto_form.html'
    success_url = reverse_lazy('desconto_list')

class DescontoUpdateView(UpdateView):
    model = Desconto
    form_class = DescontoForm
    template_name = 'controle_pagamento/desconto_form.html'
    success_url = reverse_lazy('desconto_list')

class DescontoDeleteView(DeleteView):
    model = Desconto
    template_name = 'controle_pagamento/desconto_confirm_delete.html'
    success_url = reverse_lazy('desconto_list')

class ComissaoListView(ListView):
    model = Comissao
    template_name = 'controle_pagamento/comissao_list.html'

class ComissaoDetailView(DetailView):
    model = Comissao
    template_name = 'controle_pagamento/comissao_detail.html'

class ComissaoCreateView(CreateView):
    model = Comissao
    form_class = ComissaoForm
    template_name = 'controle_pagamento/comissao_form.html'
    success_url = reverse_lazy('comissao_list')

class ComissaoUpdateView(UpdateView):
    model = Comissao
    form_class = ComissaoForm
    template_name = 'controle_pagamento/comissao_form.html'
    success_url = reverse_lazy('comissao_list')

class ComissaoDeleteView(DeleteView):
    model = Comissao
    template_name = 'controle_pagamento/comissao_confirm_delete.html'
    success_url = reverse_lazy('comissao_list')