# Biblioteca de comunicação http/https
import http.client
# Biblioteca para manipulação de json
import json

# Busca o arquivo que contém o json para Emissão de Nota Fiscal
with open('emitirNotaFiscal.json', 'r') as json_file:
   # Carrega o conteudo do arquivo e converte em array
   array = json.load(json_file)
   # Converte o array em json novamente
   json = json.dumps(array)
   
#  Define o Host para a comunicação com a API
conn = http.client.HTTPSConnection("webmaniabr.com")

# Credenciais de acesso
headers = {
    'cache-control': "no-cache",
    'content-type': "application/json",
    'x-consumer-key': "WMfBec50owmohV4V8pLkAMKKmACLTj5o",
    'x-consumer-secret': "mMTrvCcCvMv8xdNKsR2f3K4DTtBZkkVg1Eq7WRKqLGqqQ4qQ",
    'x-access-token': "5458-Yu6pZGOGuQr0CR2RYnAXfGa7tokCtF4rOO9vJzvpFSn9xVs0",
    'x-access-token-secret': "XjuBfPr1n8d6KbD78jSGmfsRMoRzpJpCoTg8rIQy3clKvcJM"
}

# Comunicando com a API
conn.request("POST", "/api/1/nfe/emissao/", json, headers)

# Retorno da API
res = conn.getresponse()
data = res.read()

# Exibir retorno
print(data.decode("utf-8"))