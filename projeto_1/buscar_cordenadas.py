"""
criei esse codigo para saber a posicao do mouse_position porque tem uma funcao que nao fucionar no script do 
mouse info
"""

import pyautogui


print('Ctrl C no terminal para o programa')
try:
    while True:
        x, y = pyautogui.position()
        posicao = f'Position x: {x} Y: {y}'
        size = pyautogui.size()
        print(f'Size: {size} {posicao} \r', end='')
    
except KeyboardInterrupt:
    print('\n')
