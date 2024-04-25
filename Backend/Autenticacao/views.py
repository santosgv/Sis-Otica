from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from .models import USUARIO
from django.contrib import auth
from django.conf import settings
from .models import Ativacao
from .utils import email_html
from hashlib import sha256
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
import logging

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
        data_nascimento = request.user.DATA_NASCIMENTO
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