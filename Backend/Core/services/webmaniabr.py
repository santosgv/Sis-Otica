import http.client
import json

'''def emitir_nfe(cliente, produtos, total):
    """
    Emite NF-e via WebmaniaBR
    :param cliente: dict com dados do cliente
    :param produtos: list de dicts com produtos
    :param total: valor total do pedido
    """

    payload = {
        "operacao": 1,
        "natureza_operacao": "Venda de produção do estabelecimento",
        "modelo": 1,
        "finalidade": 1,
        "ambiente": 2,  # 1 = produção, 2 = homologação
        "cliente": {
            "cpf": cliente["cpf"],
            "nome_completo": cliente["nome"],
            "endereco": cliente["endereco"],
            "complemento": cliente.get("complemento", ""),
            "numero": cliente.get("numero", ""),
            "bairro": cliente["bairro"],
            "cidade": cliente["cidade"],
            "uf": cliente["uf"],
            "cep": cliente["cep"],
            "telefone": cliente.get("telefone", ""),
            "email": cliente.get("email", "")
        },
        "produtos": [],
        "pedido": {
            "pagamento": 0,
            "presenca": 2,
            "modalidade_frete": 0,
            "frete": "0.00",
            "desconto": "0.00",
            "total": str(total),
            "forma_pagamento": 15
        }
    }

    # Adiciona produtos no JSON
    for p in produtos:
        payload["produtos"].append({
            "nome": p["nome"],
            "codigo": p["codigo"],
            "ncm": "6109.10.00",   # fixo
            "cest": "28.038.00",   # fixo
            "quantidade": p["quantidade"],
            "unidade": "UN",
            "peso": p.get("peso", "0.200"),
            "origem": 0,
            "subtotal": str(p["subtotal"]),
            "total": str(p["total"]),
            "impostos": {
                "icms": {
                    "codigo_cfop": "5.102",
                    "situacao_tributaria": "102"
                },
                "ipi": {
                    "situacao_tributaria": "99",
                    "codigo_enquadramento": "999",
                    "aliquota": "0.00"
                },
                "pis": {
                    "situacao_tributaria": "99",
                    "aliquota": "0.00"
                },
                "cofins": {
                    "situacao_tributaria": "99",
                    "aliquota": "0.00"
                }
            }
        })

    # Converte para JSON
    json_payload = json.dumps(payload)

    # Comunicação com WebmaniaBR
    conn = http.client.HTTPSConnection("webmaniabr.com")

    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        'x-consumer-key': "@",
        'x-consumer-secret': "@",
        'x-access-token': "5458-@",
        'x-access-token-secret': "@"
    }

    conn.request("POST", "/api/1/nfe/emissao/", json_payload, headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))
'''
import os
from decimal import Decimal
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def emitir_nfe(cliente, produtos, total, numero_nf=1, serie=1):
    """
    Gera XML da NF-e no layout SEFAZ 4.00
    (sem assinatura digital e sem envio).

    :param cliente: dict
    :param produtos: list[dict]
    :param total: Decimal ou float
    :param numero_nf: número da nota
    :param serie: série da nota
    :return: caminho do xml salvo
    """

    total = Decimal(str(total)).quantize(Decimal("0.01"))

    # ==================================================
    # TAG RAIZ
    # ==================================================
    root = Element(
        "NFe",
        xmlns="http://www.portalfiscal.inf.br/nfe"
    )

    infNFe = SubElement(
        root,
        "infNFe",
        Id=f"NFe{numero_nf:044d}",
        versao="4.00"
    )

    # ==================================================
    # IDE
    # ==================================================
    ide = SubElement(infNFe, "ide")

    campos_ide = {
        "cUF": "31",  # Minas Gerais
        "cNF": str(numero_nf).zfill(8),
        "natOp": "Venda de mercadoria",
        "mod": "55",
        "serie": str(serie),
        "nNF": str(numero_nf),
        "dhEmi": datetime.now().isoformat(),
        "tpNF": "1",
        "idDest": "1",
        "cMunFG": "3106200",  # BH (troque se quiser)
        "tpImp": "1",
        "tpEmis": "1",
        "cDV": "0",
        "tpAmb": "2",  # homologação
        "finNFe": "1",
        "indFinal": "1",
        "indPres": "1",
        "procEmi": "0",
        "verProc": "1.0"
    }

    for tag, valor in campos_ide.items():
        SubElement(ide, tag).text = valor

    # ==================================================
    # EMITENTE (SUA EMPRESA)
    # ==================================================
    emit = SubElement(infNFe, "emit")

    emitente = {
        "CNPJ": "00000000000000",
        "xNome": "MINHA EMPRESA LTDA",
        "xFant": "MINHA EMPRESA",
        "IE": "123456789",
        "CRT": "1"  # Simples Nacional
    }

    for tag, valor in emitente.items():
        SubElement(emit, tag).text = valor

    enderEmit = SubElement(emit, "enderEmit")

    endereco_emit = {
        "xLgr": "Rua Exemplo",
        "nro": "100",
        "xBairro": "Centro",
        "cMun": "3156702",
        "xMun": "Santa Luzia",
        "UF": "MG",
        "CEP": "33000000",
        "cPais": "1058",
        "xPais": "Brasil",
        "fone": "31999999999"
    }

    for tag, valor in endereco_emit.items():
        SubElement(enderEmit, tag).text = valor

    # ==================================================
    # DESTINATÁRIO
    # ==================================================
    dest = SubElement(infNFe, "dest")

    cpf = cliente.get("cpf", "").replace(".", "").replace("-", "")

    SubElement(dest, "CPF").text = cpf
    SubElement(dest, "xNome").text = cliente["nome"]

    enderDest = SubElement(dest, "enderDest")

    endereco_dest = {
        "xLgr": cliente["endereco"],
        "nro": cliente.get("numero", "S/N"),
        "xBairro": cliente["bairro"],
        "cMun": "3156702",
        "xMun": cliente["cidade"],
        "UF": cliente["uf"],
        "CEP": cliente["cep"].replace("-", ""),
        "cPais": "1058",
        "xPais": "Brasil"
    }

    for tag, valor in endereco_dest.items():
        SubElement(enderDest, tag).text = str(valor)

    # ==================================================
    # PRODUTOS
    # ==================================================
    total_produtos = Decimal("0.00")

    for index, produto in enumerate(produtos, start=1):

        subtotal = Decimal(str(produto["total"]))

        det = SubElement(
            infNFe,
            "det",
            nItem=str(index)
        )

        prod = SubElement(det, "prod")

        dados_prod = {
            "cProd": str(produto["codigo"]),
            "cEAN": "",
            "xProd": produto["nome"],
            "NCM": "61091000",
            "CFOP": "5102",
            "uCom": "UN",
            "qCom": str(produto["quantidade"]),
            "vUnCom": str(subtotal),
            "vProd": str(subtotal),
            "cEANTrib": "",
            "uTrib": "UN",
            "qTrib": str(produto["quantidade"]),
            "vUnTrib": str(subtotal),
            "indTot": "1"
        }

        for tag, valor in dados_prod.items():
            SubElement(prod, tag).text = valor

        # ==========================
        # IMPOSTOS
        # ==========================
        imposto = SubElement(det, "imposto")

        icms = SubElement(imposto, "ICMS")
        icmssn102 = SubElement(icms, "ICMSSN102")

        SubElement(icmssn102, "orig").text = "0"
        SubElement(icmssn102, "CSOSN").text = "102"

        pis = SubElement(imposto, "PIS")
        pisnt = SubElement(pis, "PISNT")

        SubElement(pisnt, "CST").text = "99"

        cofins = SubElement(imposto, "COFINS")
        cofinsnt = SubElement(cofins, "COFINSNT")

        SubElement(cofinsnt, "CST").text = "99"

        total_produtos += subtotal

    # ==================================================
    # TOTAL
    # ==================================================
    total_tag = SubElement(infNFe, "total")
    icmsTot = SubElement(total_tag, "ICMSTot")

    totais = {
        "vBC": "0.00",
        "vICMS": "0.00",
        "vICMSDeson": "0.00",
        "vFCP": "0.00",
        "vBCST": "0.00",
        "vST": "0.00",
        "vFCPST": "0.00",
        "vFCPSTRet": "0.00",
        "vProd": str(total_produtos),
        "vFrete": "0.00",
        "vSeg": "0.00",
        "vDesc": "0.00",
        "vII": "0.00",
        "vIPI": "0.00",
        "vIPIDevol": "0.00",
        "vPIS": "0.00",
        "vCOFINS": "0.00",
        "vOutro": "0.00",
        "vNF": str(total)
    }

    for tag, valor in totais.items():
        SubElement(icmsTot, tag).text = valor

    # ==================================================
    # PAGAMENTO
    # ==================================================
    pag = SubElement(infNFe, "pag")
    detPag = SubElement(pag, "detPag")

    SubElement(detPag, "tPag").text = "15"
    SubElement(detPag, "vPag").text = str(total)

    # ==================================================
    # GERA XML FORMATADO
    # ==================================================
    xml_bytes = tostring(root, encoding="utf-8")
    xml_formatado = minidom.parseString(xml_bytes).toprettyxml(indent="  ")

    # ==================================================
    # SALVAR ARQUIVO
    # ==================================================
    pasta = "xml_nfe"
    os.makedirs(pasta, exist_ok=True)

    caminho_arquivo = os.path.join(
        pasta,
        f"nfe_{numero_nf}.xml"
    )

    with open(caminho_arquivo, "w", encoding="utf-8") as file:
        file.write(xml_formatado)

    return caminho_arquivo