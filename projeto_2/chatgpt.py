"""
Ajuste fino:
 Na documentacao gemini tem explicacao de como colocar ajuste fino que e fazer a maquina aprender algo que eu quero,
 pode ser tipo me passando a medida de um diamentro de uma pizza ou com qualquer outra coisa tipo para saber o crescimento
 de algo e ela ja me passa a resposta de um posssivel futuro como se fosse uma bola de neve OBS:(Eu estou deduzindo isso
 pelo que eu li na documentacao do gemini)

Aprimorar a formataçao:
 tenho que criar uma funcao mais aprimorada para seperar o codigo formatar ele bonitinho retornando possivelmente uma cor
 diferente tipo que ele seja copiado sozinho.

Aprimorar o codigo:
 tenho que aprimorar o codigo apagando coisas que ja foi usada
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os
_ = 80 * '_'


def formatar_texto(texto):
    """
    Formata um texto, quebrando linhas para melhor legibilidade.

    Args:
        texto: O texto a ser formatado.

    Returns:
        O texto formatado.
    """
    linhas = texto.split('\n')  # Separa o texto em linhas
    formatado = ''

    for linha in linhas:
        linha = linha.strip('*')  # Remove o asterisco e o espaço
        nova_linha = linha.replace("**", "")  # Remove o asterico do meio da string
        formatado += f'{nova_linha}\n'  # Adiciona um marcador numérico e quebra de linha

    return formatado


class ChatGpt:
    """
    Classe para interagir com o modelo de linguagem ChatGPT da Google.
    """
    def __init__(self, api_key=None, modelo=None, chat=None, model_info=None, total_tokens=0):
        """
        Inicializa a classe ChatGpt.

        Args:
            api_key: Chave de API para acessar o serviço do Google Generative AI.
            modelo: Nome do modelo de linguagem a ser usado.
            chat: Instância do chat em andamento.
            model_info: Informações sobre o modelo de linguagem.
            total_tokens: Número total de tokens usados na conversa.
        """
        self.model_info = model_info
        self.resposta = 'Error ao executar sua resposta por favor tente mais tarde, se continuar sem fucionar o Tiago vai tentar resolver o error'
        self.chat = chat
        self.modelo = modelo
        self.api_key = api_key
        self.dados = ''
        self.total_tokens = total_tokens

    def sua_resposta(self):
        """
        Retorna a resposta formatada com uma linha de separação.

        Returns:
            str: A resposta formatada.
        """
        text = self.resposta
        self.resposta = 'Faça uma pergunta\n'
        return text

    def enviar_mensagem(self, pergunta_):
        """
        Envia uma mensagem para o ChatGPT e armazena a resposta.

        Args:
            pergunta_: A pergunta a ser enviada.
        """
        if self.chat is None:
            erro = 'Você deve configurar seu chat primeiro.'
            with open('log_gptflash.txt', 'a+') as file:
                file.write(f'Error: {erro}\n')
                file.close()
            return

        try:
            response = self.chat.send_message(pergunta_,
                                              generation_config=genai.types.GenerationConfig(max_output_tokens=10000,
                                                                                             temperature=1.0))
            self.resposta = formatar_texto(response.text)
            return

        except Exception as error:
            erro = f'Error ao enviar mensagem: {error}'
            with open('log_gptflash.txt', 'a+') as file:
                file.write(f'Error: {erro}\n')
                file.close()

    def config_gpt(self):
        """
        Configura a conexão com o ChatGPT, carregando a chave de API e criando o chat.
        """
        load_dotenv()
        self.api_key = os.getenv('chave_gemini')
        try:
            genai.configure(api_key=self.api_key)

            # Criar o modelo de chat
            # system_instruction recebe algo inicial que queira que o chat seja tenho que arrumar
            # na apresentacao de quem e o gemini
            self.modelo = genai.GenerativeModel("gemini-1.5-flash", #  o modelo pro nao esta fucionando por enquanto
                                                system_instruction="""Voce e uma mulher, nasceu em 9 de julho de 2009 mas
                                                                   nao e necessario voce falar quando voce nasceu somente
                                                                   quando o usuario te perguntar e seu nome e Ana Beatriz""", )
            self.chat = self.modelo.start_chat(history=[])

        except Exception as error:
            erro = f'Falha ao configurar o GPT: {error}'
            with open('log_gptflash.txt', 'a+') as file:
                file.write(f'Error: {erro}\n{_}\n')
                file.close()

    #  caso queira testar aqui mesmo utilize essa funcao
    def iniciar_chat(self):
        """
        Inicia uma sessão de chat interativa com o ChatGPT.
        """
        print("Você pode começar a conversar! Digite 'sair' para encerrar o chat.")
        while True:
            user_input = input("Você: ")
            if user_input.lower() == 'sair':
                print("Chat encerrado.")
                break

            # Verificar se o chat está configurado antes de mandar qualquer mensagem
            if self.chat is None:
                print('Você deve configurar seu chat primeiro.')
                return

            # Enviar mensagem para o chat e obter resposta
            try:
                # estou testando sobre essa generation_config
                response = self.chat.send_message(user_input, generation_config=genai.types.GenerationConfig())
                print()
                print('Ana: ', response.text, '\n', _)

                #  teste de como contar token para um possivel limitacao de conversa
                self.infos_token(chat_history=self.chat)
                if self.total_tokens >= 2000:
                    print(f'ultrapassou 2k de tokens')
                    continue

            except Exception as erro:
                with open('log_gptflash.txt', 'a+') as file:
                    file.write(f'Error: {erro}\n{_}\n')

    #  Falta somar a entrada com o chat history porque sao separados diferentes e ainda nao utilizo essa funçao
    def infos_token(self, chat_history=None, tokens_info=False, entrada=None, saida=None):
        """
        Coleta e exibe informações sobre o uso de tokens na conversa.

        Args:
            chat_history: Histórico da conversa.
            tokens_info: Sinaliza se as informações sobre os limites de tokens devem ser exibidas.
            entrada: Texto de entrada para o modelo.
            saida: Resposta do modelo.
        """
        nome = f'models/gemini-1.5-flash'  #  aprimorar como o modelo vai ser escolhido
        model_info = genai.get_model(nome)
        model = genai.GenerativeModel(nome)

        #  conta os tokens de entrada e saida
        if entrada is not None:
            print(f'Total tokens entrada\n{model.count_tokens(entrada)}')
            if saida is not None:
                print(f'Total tokens saida\n{model.count_tokens(saida.text)}')
                return
            return

        #  provavelmente no futuro irei colocar uma codicao que bloqueia pelo tokens
        #  utilizando o chat_history
        elif chat_history is not None:
            result = model.count_tokens(chat_history.history)
            total = int(result.total_tokens)
            # print(total)  #  apareceu a qtd
            self.total_tokens = total
            return

        #  Essa condiçao me passa o limit total de tokens da saida e entrada
        elif tokens_info:
            entrada_ = f"{model_info.input_token_limit=}"
            saida_ = f"{model_info.output_token_limit=}"
            print(entrada_, saida_)
            return
        return


# Iniciar o chat interativo
if __name__ == '__main__':
    gpt = ChatGpt()
    gpt.config_gpt()  #  inicia umas config para usar o chat
    gpt.iniciar_chat()  #  inicia uma conversa com o chat