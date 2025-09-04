import http.client
import json

def emitir_nfe(request,cliente, produtos, total):
    from Core.utils import get_tenant

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
        'x-consumer-key': f"{get_tenant(request).consumer_key}",
        'x-consumer-secret': f"{get_tenant(request).consumer_secret}",
        'x-access-token': f"{get_tenant(request).access_token}",
        'x-access-token-secret': f"{get_tenant(request).access_token_secret}"
    }

    conn.request("POST", "/api/1/nfe/emissao/", json_payload, headers)

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))
