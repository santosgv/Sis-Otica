from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import redirect
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
import logging
from django.http import FileResponse


logger = logging.getLogger('MyApp')

def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)
    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}

def calcular_inss(salario_bruto):
    if salario_bruto <= 1100:
        return round(salario_bruto * 0.075,2)
    elif 1100.01 <= salario_bruto <= 2203.48:
        return round(salario_bruto * 0.09,2)
    elif 2203.49 <= salario_bruto <= 3305.22:
        return round(salario_bruto * 0.12,2)
    elif 3305.23 <= salario_bruto <= 6433.57:
        return round(salario_bruto * 0.14,2)
    else:
        return 751.99 

def calcular_irrf(salario_liquido):
    if salario_liquido <= 1903.98:
        return 0
    elif 1903.99 <= salario_liquido <= 2826.65:
        return round((salario_liquido * 0.075) - 142.8,2)
    elif 2826.66 <= salario_liquido <= 3751.05:
        return round((salario_liquido * 0.15) - 354.8,2)
    elif 3751.06 <= salario_liquido <= 4664.68:
        return round((salario_liquido * 0.225) - 636.13,2)
    else:
        return round((salario_liquido * 0.275) - 869.36,2)

def generate_pdf(nome_empresa, endereco, cnpj, mes_corrente, id_colaborador,colaborador,cargo,dataadminissao,horas_extras,total_comissao,comissoes,descontos,inss, salario_liquido, total_descontos, salario_bruto, desconto_irrf):
    coordenadas = {
        'Nome_Empresa': (84, 732),
        'Endereco': (105, 714),
        'CNPJ': (82, 695),
        'Mes_Corrente': (475, 695),

        'id':(50,645),
        'Funcionario':(105,645),
        'Cargo':(258,645),
        'Admissao':(440,645),

        'horas_extra':(45,555),
        'comissao':(45,543),
        'total_comissao':(45,285),
        #'inss':(380,555),
        'desconto':(380,520),
        

        'total_desconto':(498, 223),
        'saldo_liquido':(498, 197),
        'salario_base':(50, 150),
        'inss':(355, 150),
        'irrf':(485, 150),


    }
    try:
        buffer = io.BytesIO()
        PDF = canvas.Canvas(buffer,pagesize=letter)
        PDF.setFont('Courier-Bold', 15)
        PDF.drawImage(os.path.join(settings.BASE_DIR, 'templates','holerite.png'),0, 0, width=letter[0], height=letter[1])
        PDF.drawString(coordenadas['Nome_Empresa'][0], coordenadas['Nome_Empresa'][1],str(f'{nome_empresa}'))
        PDF.drawString(coordenadas['Endereco'][0], coordenadas['Endereco'][1],str(f'{endereco}'))
        PDF.drawString(coordenadas['CNPJ'][0], coordenadas['CNPJ'][1],str(f'{cnpj}'))
        PDF.drawString(coordenadas['Mes_Corrente'][0], coordenadas['Mes_Corrente'][1],str(f'{mes_corrente}'))

        PDF.setFont('Courier-Bold', 12)
        PDF.drawString(coordenadas['id'][0], coordenadas['id'][1],str(f'{id_colaborador}'))
        PDF.drawString(coordenadas['Funcionario'][0], coordenadas['Funcionario'][1],str(f'{colaborador}'))
        PDF.drawString(coordenadas['Cargo'][0], coordenadas['Cargo'][1],str(f'{cargo}'))
        PDF.drawString(coordenadas['Admissao'][0], coordenadas['Admissao'][1],str(f'{dataadminissao}'))



        PDF.drawString(coordenadas['horas_extra'][0], coordenadas['horas_extra'][1],str(f'Horas Extras: R${horas_extras}'))
        PDF.setFont('Courier-Bold', 12)
        y_comissao = coordenadas['comissao'][1]
        for comissao in comissoes:
            PDF.drawString(coordenadas['comissao'][0], y_comissao, f'Comissão R${comissao.valor_vendas} x {comissao.colaborador.comissao_percentual}%')
            y_comissao -= 15 

        y_desconto = coordenadas['desconto'][1]
        for desconto in descontos:
            PDF.drawString(coordenadas['desconto'][0], y_desconto, f'{desconto.tipo} {desconto.percentual}%')
            y_desconto -= 15 
        #PDF.drawString(coordenadas['inss'][0], coordenadas['inss'][1],str(f'Desconto INSS: R${inss}'))
        #PDF.drawString(380,540,str(f'Desconto IRRF: R${desconto_irrf}'))

        PDF.drawString(coordenadas['total_comissao'][0], coordenadas['total_comissao'][1],str(f'Total Comissao: R${total_comissao}'))
        PDF.setFont('Courier-Bold', 12)
        PDF.drawString(coordenadas['total_desconto'][0], coordenadas['total_desconto'][1],str(f'{total_descontos}'))
        PDF.drawString(coordenadas['saldo_liquido'][0], coordenadas['saldo_liquido'][1],str(f'{salario_liquido}'))
        PDF.drawString(coordenadas['salario_base'][0], coordenadas['salario_base'][1],str(f'{salario_bruto}'))
        PDF.drawString(coordenadas['inss'][0], coordenadas['inss'][1],str(f'{inss}'))
        PDF.drawString(coordenadas['irrf'][0], coordenadas['irrf'][1],str(f'{desconto_irrf}'))

        PDF.showPage()
        PDF.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'holerite.pdf')
    except Exception as msg:
        logger.critical(msg)
        return redirect('/auth/listar_folha_pagamento')