"""
Para usar esse script confira se voce possui um programa aberto onde vai digitar seus dados e sempre passe
as cordenadas certas para saber as cordenadas exatas use o mouseInfo() do pyautogui ou crie um script para
conferir as cordenadas com pyautogui
"""

import openpyxl
import pyautogui
from pathlib import Path
import time

base = Path(__file__).parent
caminho_planilha = base / 'vendas_de_produtos.xlsx'

p = openpyxl.load_workbook(caminho_planilha)
p_vendas = p['vendas']


def criar_e_salvar(x, y, dados:str):
    """
    x e y sao cordenadas que recebe do usuario onde clicar e digitar os dados da planilha que abriu

    dados vem da planilha que voce abriu e desempacota para ficar mais facil escrever no seu programa
    """

    pyautogui.click(x, y, interval=0.25)
    pyautogui.write(dados)


for v in p_vendas.iter_rows(values_only=True, min_row=2):
    cliente, produto, quantidade, categoria = v
    
    # cliente x 1201 y 446
    criar_e_salvar(1201, 446, str(cliente))
    time.sleep(3)

    # produto x 1192 y 496
    criar_e_salvar(1192, 496, str(produto))
    time.sleep(3)

    # quantidade x 1212 y 552
    criar_e_salvar(1212, 552, str(quantidade))
    time.sleep(3)

    # categoria produto x 1192 y 606
    criar_e_salvar(1192, 606, str(categoria))

    # salvar x 1036 y 657
    pyautogui.moveTo(1036, 657)
    pyautogui.click()
