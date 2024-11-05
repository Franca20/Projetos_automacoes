import requests
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from chatgpt import ChatGpt
import time
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# configurando meu gpt antes de iniciar
chatgpt_ = ChatGpt()
chatgpt_.config_gpt()


def get_url_cep(cep):
    if len(cep) == 1:
        if cep[0].isnumeric() and len(cep[0]) == 8:

            valor = requests.get(f"http://viacep.com.br/ws/{cep[0]}/json")
            try:
                if valor.status_code == 200:
                    res = valor.json()

                    cidade = res['localidade']
                    logradouro = res['logradouro']
                    bairro = res['bairro']
                    estado = res['uf']
                    regiao = res['regiao']

                    return f'CEP {cep[0]}\nRegiao: {regiao}\nEstado: {estado}\nCidade: {cidade}\nRua: {logradouro}\nBairro: {bairro}'

                else:
                    return 'Site ou cep inexistente, por favor tente outro cep'

            except Exception as e:
                with open('logs.txt', 'a+') as file:
                    file.close()
            
        return 'cep invalido'
    return 'cep invalido'

def get_url_dog():
    foto_dog = requests.get('https://random.dog/woof.json').json()
    url_dog = foto_dog['url']
    return url_dog

async def bop(update:Update, context: ContextTypes.DEFAULT_TYPE):
    url_dog = get_url_dog()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url_dog)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Comandos:\n/help -> mostra comandos\n\n/bop -> para ver imagens aleatorias de cachorros\n\n/cep numeros -> Buscar dados do local\n\nPara conversar com o chatgpt basta voce escrever sem comando nenhum que a Ana lhe responderar")

async def chat_gpt(update:Update, context: ContextTypes.DEFAULT_TYPE):
    chatgpt_.enviar_mensagem(update.message.text)
    time.sleep(3)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=chatgpt_.sua_resposta())

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='digite "/help" para ver os comandos')

# Apenas teste da documentacao para criar comandos que eu consiga fazer alteracoes
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def cep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cep_retorno = get_url_cep(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=cep_retorno)

if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(os.getenv('token_telegram')).build()
        
        start_handler = CommandHandler('start', start)
        help_handler = CommandHandler('help', help)
        bop_handler = CommandHandler('bop', bop)
        gpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat_gpt)

        # das novas funcoes
        caps_handler = CommandHandler('caps', caps)
        cep_handler = CommandHandler('cep', cep)

        lista_handlers = [help_handler, bop_handler, gpt_handler, start_handler, caps_handler, cep_handler, ]
        application.add_handlers(lista_handlers)
        
        application.run_polling()
    except KeyboardInterrupt:
        print()