from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import date
from calendar import monthrange
from Autenticacao.models import USUARIO, Comissao, Desconto
from django.http import HttpResponse, FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from django.conf import settings

def generate_pdf(
    nome_empresa,
    endereco,
    cnpj,
    mes_corrente,
    id_colaborador,
    colaborador,
    cargo,
    data_admissao,
    horas_extras,
    total_comissao,
    comissoes,
    descontos,
    inss,
    salario_liquido,
    total_descontos,
    salario_bruto,
    desconto_irrf,
    desconto_fgts
):
    coordenadas = {
        'Nome_Empresa': (84, 732),
        'Endereco': (105, 714),
        'CNPJ': (82, 695),
        'Mes_Corrente': (475, 695),
        'id': (50, 645),
        'Funcionario': (105, 645),
        'Cargo': (258, 645),
        'Admissao': (440, 645),
        'horas_extra': (45, 555),
        'comissao': (45, 543),
        'total_comissao': (45, 285),
        'desconto': (380, 520),
        'total_desconto': (498, 223),
        'saldo_liquido': (498, 197),
        'salario_base': (50, 150),
        'inss': (355, 150),
        'fgts': (270, 150),
        'fgts1': (150, 150),
        'irrf': (485, 150),
    }
    try:
        buffer = io.BytesIO()
        PDF = canvas.Canvas(buffer, pagesize=letter)
        PDF.setFont('Courier-Bold', 15)
        PDF.drawImage(os.path.join(settings.BASE_DIR, 'templates', 'holerite.png'), 0, 0, width=letter[0], height=letter[1])
        PDF.drawString(coordenadas['Nome_Empresa'][0], coordenadas['Nome_Empresa'][1], str(nome_empresa))
        PDF.drawString(coordenadas['Endereco'][0], coordenadas['Endereco'][1], str(endereco))
        PDF.drawString(coordenadas['CNPJ'][0], coordenadas['CNPJ'][1], str(cnpj))
        PDF.drawString(coordenadas['Mes_Corrente'][0], coordenadas['Mes_Corrente'][1], str(mes_corrente))
        
        PDF.setFont('Courier-Bold', 12)
        PDF.drawString(coordenadas['id'][0], coordenadas['id'][1], str(id_colaborador))
        PDF.drawString(coordenadas['Funcionario'][0], coordenadas['Funcionario'][1], str(colaborador))
        PDF.drawString(coordenadas['Cargo'][0], coordenadas['Cargo'][1], str(cargo))
        PDF.drawString(coordenadas['Admissao'][0], coordenadas['Admissao'][1], str(data_admissao))

        PDF.drawString(coordenadas['horas_extra'][0], coordenadas['horas_extra'][1], f'Horas Extras: R${horas_extras:.2f}')
        
        y_comissao = coordenadas['comissao'][1]
        for comissao in comissoes:
            PDF.drawString(coordenadas['comissao'][0], y_comissao, f'Comissão R${comissao["valor_vendas"]:.2f} x {comissao["percentual"]}%')
            y_comissao -= 15 

        y_desconto = coordenadas['desconto'][1]
        for desconto in descontos:
            PDF.drawString(coordenadas['desconto'][0], y_desconto, f'{desconto["tipo"]} {desconto["percentual"]}')
            y_desconto -= 15 

        PDF.drawString(coordenadas['total_comissao'][0], coordenadas['total_comissao'][1], f'Total Comissão: R${total_comissao:.2f}')
        PDF.drawString(coordenadas['total_desconto'][0], coordenadas['total_desconto'][1], f'R${total_descontos:.2f}')
        PDF.drawString(coordenadas['saldo_liquido'][0], coordenadas['saldo_liquido'][1], f'R${salario_liquido:.2f}')
        PDF.drawString(coordenadas['salario_base'][0], coordenadas['salario_base'][1], f'R${salario_bruto:.2f}')
        PDF.drawString(coordenadas['inss'][0], coordenadas['inss'][1], f'R${inss:.2f}')
        PDF.drawString(coordenadas['fgts'][0], coordenadas['fgts'][1], f'R${desconto_fgts:.2f}')
        PDF.drawString(coordenadas['fgts1'][0], coordenadas['fgts1'][1], f'R${desconto_fgts:.2f}')
        PDF.drawString(coordenadas['irrf'][0], coordenadas['irrf'][1], f'R${desconto_irrf:.2f}')

        PDF.showPage()
        PDF.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'holerite_{id_colaborador}_{mes_corrente.replace("/", "-")}.pdf')
    except Exception as msg:
        print(f"Erro ao gerar PDF: {msg}")
        return HttpResponse({"error": str(msg)}, status=500, content_type="application/json")

def baixar_pdf(request, colaborador_id, referencia):
    try:
        # Validar formato da referência (AAAA-MM)
        partes = referencia.split('-')
        if len(partes) != 2:
            return HttpResponse(
                {"error": "Formato de referência inválido. Use AAAA-MM."},
                status=400,
                content_type="application/json"
            )
        ano = int(partes[0])
        mes = int(partes[1])
        primeiro_dia = date(ano, mes, 1)
        ultimo_dia = date(ano, mes, monthrange(ano, mes)[1])

        # Buscar colaborador
        colaborador = get_object_or_404(USUARIO, pk=colaborador_id)

        # Mapear função
        funcao_map = {
            'G': 'Gerente',
            'V': 'Vendedor',
            'C': 'Caixa'
        }
        funcao = funcao_map.get(colaborador.FUNCAO, 'Caixa')

        # Salário bruto
        salario_bruto = colaborador.salario_bruto

        # Buscar comissões no intervalo de referência
        comissoes = Comissao.objects.filter(
            colaborador=colaborador,
            data_referencia__range=(primeiro_dia, ultimo_dia)
        )

        # Calcular comissões e horas extras
        comissoes_detalhadas = []
        total_comissao = 0
        total_horas_extras = 0
        for c in comissoes:
            valor_comissao = c.calcular_comissao()
            valor_horas = c.calcula_horas_extras()
            total_comissao += valor_comissao
            total_horas_extras += valor_horas
            comissoes_detalhadas.append({
                "valor_vendas": c.valor_vendas,
                "percentual": colaborador.comissao_percentual,
                "comissao_gerada": round(valor_comissao, 2),
                "horas_extras": c.horas_extras,
                "valor_hora": colaborador.valor_hora,
                "horas_extras_valor": round(valor_horas, 2)
            })

        # Buscar descontos
        descontos = Desconto.objects.filter(colaborador=colaborador)
        descontos_data = []
        total_descontos = 0
        for d in descontos:
            valor_desconto = salario_bruto * (d.percentual / 100)
            total_descontos += valor_desconto
            descontos_data.append({
                "tipo": d.tipo,
                "percentual": f"{d.percentual}%",
                "valor": round(valor_desconto, 2)
            })

        # Descontos fixos
        desconto_inss = round(salario_bruto * 0.075, 2)
        desconto_fgts = round(salario_bruto * 0.08, 2)
        salario_liquido_parcial = salario_bruto + total_comissao + total_horas_extras - total_descontos - desconto_inss - desconto_fgts
        desconto_irrf = 0  # Supondo função definida
        total_descontos += desconto_inss + desconto_fgts + desconto_irrf

        # Salário líquido final
        salario_liquido = salario_bruto + total_comissao + total_horas_extras - total_descontos

        # Gerar o PDF
        pdf_response = generate_pdf(
            nome_empresa="Nome Empresa Aqui",
            endereco="Endereço Aqui",
            cnpj="CNPJ Aqui",
            mes_corrente=f"{mes:02d}/{ano}",
            id_colaborador=colaborador.id,
            cargo=funcao,
            data_admissao=colaborador.data_contratacao,
            horas_extras=round(total_horas_extras, 2),
            comissoes=comissoes_detalhadas,
            total_comissao=round(total_comissao, 2),
            descontos=descontos_data,
            inss=desconto_inss,
            colaborador=colaborador.first_name,
            salario_liquido=round(salario_liquido, 2),
            total_descontos=round(total_descontos, 2),
            salario_bruto=round(salario_bruto, 2),
            desconto_irrf=round(desconto_irrf, 2),
            desconto_fgts=desconto_fgts
        )
        return pdf_response

    except Exception as e:
        print(e)
        return HttpResponse(
            {"error": str(e)},
            status=500,
            content_type="application/json"
        )