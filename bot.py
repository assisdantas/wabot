import os
import time
import re
import requests
import json
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver



class wppbot:

    dir_path = os.getcwd()

    def __init__(self, nome_bot):

        print('[*] Iniciando em: ' + self.dir_path)
        print('')
        print('[i] Pré aprendizado... Saída do nltk:')
        print('') 

        self.bot = ChatBot(nome_bot)
        self.trainer = ListTrainer(self.bot)

        self.chrome = self.dir_path+'/chromedriver'
        print('''[i] Pré aprendizado... ''')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"/profile/wpp")
        #self.options.add_argument('--headless')
        #self.options.add_argument('--no-sandbox')
        #self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    def inicia(self,nome_contato):
        print('''[i] Iniciando driver em: %s/crhomedriver... ''' %self.dir_path)
        self.driver.get('https://web.whatsapp.com/')
        print('''[i] Aguardando abertura da página e leitura do QR Code se necessário...''')
        self.driver.implicitly_wait(20)

        self.caixa_de_pesquisa = self.driver.find_element_by_xpath("//div[contains(@class, '2S1VP')]")

        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        print('''[i] Entrando em contato com: %s''' %nome_contato)
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)
        print('''[i] Enviando mensagem de saudação... ''')

    def saudacao(self,frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text" and @data-tab="1"]')

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)
                self.botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
                self.botao_enviar.click()
                time.sleep(1)
                print('''[i] Mensagens de saudação enviadas. ''')
        else:
            return False

    def escuta(self):
        
        post = self.driver.find_elements_by_class_name('_3_7SH')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        return texto
        print('''[i] Texto recebido: %s ''' %texto)

    def aprender(self,ultimo_texto,frase_inicial,frase_final,frase_erro):
        self.caixa_de_mensagem = self.driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text" and @data-tab="1"]')
        self.caixa_de_mensagem.send_keys(frase_inicial)
        print('''[i] Iniciando processo de aprendizado... ''')
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
        self.botao_enviar.click()
        self.x = True
        while self.x == True:
            texto = self.escuta()

            if texto != ultimo_texto and re.match(r'^::', texto):
                if texto.find('?') != -1:
                    ultimo_texto = texto
                    texto = texto.replace('::', '')
                    texto = texto.lower()
                    texto = texto.replace('?', '?*')
                    texto = texto.split('*')
                    novo = []
                    for elemento in texto:
                        elemento = elemento.strip()
                        novo.append(elemento)

                    print('''[i] Absorvendo nova informação... ''')
                    self.trainer.train(novo)
                    print('''[i] Absorvendo nova informação... [OK] ''')
                    self.caixa_de_mensagem.send_keys(frase_final)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
                else:
                    print('''[i] Absorvendo nova informação... [FALHA] ''')
                    self.caixa_de_mensagem.send_keys(frase_erro)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
            else:
                ultimo_texto = texto

    def noticias(self):

        req = requests.get('https://newsapi.org/v2/top-headlines?sources=globo&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')
        noticias = json.loads(req.text)

        self.caixa_de_mensagem.send_keys('ELA BOT: Aqui estão algumas das ultimas notícias.')
        self.botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
        self.botao_enviar.click()
        time.sleep(1)
        
        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'ELA BOT: ' + titulo + ' ' + link + '\n'

            self.caixa_de_mensagem.send_keys(new)
            time.sleep(1)

    def responde(self,texto):
        response = self.bot.get_response(texto)
        print('Confiança da resposta: ' + str(response.confidence))
        print('Possível resposta: %s' %response)
        if float(response.confidence) > 0.5:
            response = str(response)
            response = 'ELA BOT: ' + response
            self.caixa_de_mensagem = self.driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text" and @data-tab="1"]')
            self.caixa_de_mensagem.send_keys(response)
            time.sleep(1)
            self.botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
            self.botao_enviar.click()
        else:
            self.caixa_de_mensagem = self.driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text" and @data-tab="1"]')
            self.caixa_de_mensagem.send_keys('ELA BOT: Eu ainda não sei responder esta pergunta... Desculpe.')
            time.sleep(1)
            self.botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
            self.botao_enviar.click()

    def treina(self,treina):
        for treino in os.listdir(treina):
            conversas = open(treina+'/'+treino, 'r').readlines()
            self.trainer.train(conversas)
