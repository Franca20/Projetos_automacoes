"""
Precisamos que você crie uma maneira eficiente de extrair dados do registro da Companies House do Reino Unido. O objetivo é reunir informações da empresa (colunas necessárias: Nome da empresa, Pessoas, Data de incorporação) e extraí-las em um formato CSV.
Site: https://find-and-update.company-information.service.gov.uk/

nome de empresas do reino unido para teste:

Legal & General Group plc
Antofagasta plc
Tesco plc
SSE plc
Imperial Brands plc
Standard Chartered plc
Ashtead Group plc
Ferguson plc
Vodafone Group plc
Barclays plc
NatWest Group plc
"""
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
from pathlib import Path
import os

base = Path(__file__).parent
caminho_pasta_csv = base / 'web_scrap'
name_file = caminho_pasta_csv / 'dados_empresas_uk.csv'

if not os.path.exists(caminho_pasta_csv):
    os.makedirs(caminho_pasta_csv, exist_ok=True)

    with open(name_file, mode='w') as file:
        dados = 'Empresa', 'Incorporada em', 'Pessoas'
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(dados)
        file.close

dados_completos = []

url_busca = 'https://find-and-update.company-information.service.gov.uk/'
# nome da empresa
nome_empresa = input('Digite o apenas um nome da empresa completo: ')
# pessoas e a data de incorporacao

driver = webdriver.Chrome()
driver.get(url_busca)
time.sleep(3)

id_pesquisa = 'site-search-text'
input_pesquisa = driver.find_element(by=By.ID, value=id_pesquisa)
input_pesquisa.send_keys(nome_empresa)
input_pesquisa.send_keys(Keys.ENTER)
time.sleep(8)

empresas = driver.find_elements(by=By.CLASS_NAME, value='govuk-link')
try:
    for empresa in empresas:
        if empresa.text.lower() == nome_empresa.lower():
            # adicionando nome da empresa
            dados_completos.append(empresa.text) # nome da empresa ok

            empresa_ = driver.find_element(by=By.XPATH, value='/html/body/div[1]/main/div[3]/div/div[2]/div/article/ul/li[1]/h3/a')
            empresa_.send_keys(Keys.ENTER)
            time.sleep(5)
            
            # adicionando data da incorporacao
            data_incorporada = driver.find_element(by=By.ID, value='company-creation-date')
            dados_completos.append(data_incorporada.text) # data incorporacao ok
            time.sleep(3)

            pessoas_empresa = driver.find_element(by=By.ID, value='people-tab')
            pessoas_empresa.send_keys(Keys.ENTER)
            time.sleep(5)

            #  buscando total de pessoas
            total_pessoa = driver.find_element(by=By.ID, value="company-appointments")
            numeros = re.findall(r'[0-9]+', total_pessoa.text)

            def interando_pessoas():
                """
                Essa funcao pega todas pessoas ative como resignada
                """
                c = 36
                lista_pessoas = []
                for v1 in range(c):
                    if v1 == 0:
                        continue
                    try:
                        pessoa = driver.find_element(by=By.ID, value=f'officer-name-{v1}')
                        lista_pessoas.append(pessoa.text)
                    except:
                        return lista_pessoas
                return lista_pessoas
            

            n_pessoas = int(numeros[0])
            lista_total_pessoa = []

            #  Tentei de varias formas mais a melhor forma e usando uma lista de xpath para buscar a prox pag
            lista_xpath_pag_pessoas = ['/html/body/div[1]/main/div[4]/div[2]/div/ul[2]/li[2]/a', '/html/body/div[1]/main/div[4]/div[2]/div/ul[2]/li[3]/a', '/html/body/div[1]/main/div[4]/div[2]/div/ul[2]/li[4]/a', '/html/body/div[1]/main/div[4]/div[2]/div/ul[2]/li[5]/a']

            p_pag = 1

            if not n_pessoas % 35 == 0:
                valor = int(n_pessoas / 35) + 1
                
                for v in range(valor):
                    # pegar pessoas da primera pag
                    if p_pag == 1:
                        lista_nomes = interando_pessoas()
                        lista_total_pessoa.append(lista_nomes)
                        p_pag = 0

                    # mudar pag
                    valor_xpath = lista_xpath_pag_pessoas[v]
                    proxima_pag = driver.find_element(by=By.XPATH, value=valor_xpath)
                    proxima_pag.send_keys(Keys.ENTER)

                    lista_nomes = interando_pessoas()
                    if lista_nomes in lista_total_pessoa:
                        continue
                    lista_total_pessoa.append(lista_nomes)

                    
            else:
                valor = int(n_pessoas / 35)

                for v in range(valor):
                    # pegar pessoas da primera pag
                    if p_pag == 1:
                        lista_nomes = interando_pessoas()
                        lista_total_pessoa.append(lista_nomes)
                        p_pag = 0

                    # mudar pag
                    valor_xpath = lista_xpath_pag_pessoas[v]
                    proxima_pag = driver.find_element(by=By.XPATH, value=valor_xpath)
                    proxima_pag.send_keys(Keys.ENTER)

                    lista_nomes = interando_pessoas()
                    if lista_nomes in lista_total_pessoa:
                        continue
                    lista_total_pessoa.append(lista_nomes)

            dados_completos.append(lista_total_pessoa) # lista de pessoas ok

            #  agora vou pegar os valores (nome da empresa, data incorporacao, pessoas) e escrever em csv
            def escrever_csv(empresa, data_incorporacao, pessoas:list):
                lista_juntas = []
                
                lista_juntas.append(empresa)
                lista_juntas.append(data_incorporacao)

                lista_nome = []

                for v in range(len(pessoas)):
                    for v1 in pessoas[v]:
                        lista_nome.append(v1)
                
                lista_juntas.append(lista_nome)

                with open(name_file, mode='a+') as employee_file:
                    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    employee_writer.writerow(lista_juntas)
                    employee_file.close

                return
            
            escrever_csv(empresa=dados_completos[0], data_incorporacao=dados_completos[1], pessoas=dados_completos[2])
except Exception as e:
    pass

driver.quit()