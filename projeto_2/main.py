"""
Usando API para buscar o resultados de um cep que o usuario digitar
"""

import requests

cep = 65904700

valor = requests.get(f"http://viacep.com.br/ws/{cep}/json")
print(valor)
try:
    if valor.status_code == 200:
        res = valor.json()

        cidade = res['localidade']
        logradouro = res['logradouro']
        bairro = res['bairro']
        estado = res['uf']
        regiao = res['regiao']

        print(regiao, estado, cidade, logradouro, bairro)

    else:
        print('Site ou cep inexistente, por favor tente outro cep')

except Exception as e:
    print(e)