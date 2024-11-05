import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
token_telegram = os.getenv('token_telegram')
url_base_telegram = f"https://api.telegram.org/bot{token_telegram}"

try:
    while True:
        post_telegram = requests.get(f"{url_base_telegram}/getUpdates")
        resposta_dict = post_telegram.json()
        print(resposta_dict)
        time.sleep(5)

except KeyboardInterrupt:
    print('\n')