from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


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
