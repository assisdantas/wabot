# -*- coding: utf-8 -*-

import re
from bot import wppbot

bot = wppbot('ELA')
bot.treina('treino')
bot.inicia('Casa da mamae')
bot.saudacao(['ELA BOT: Olá, me chamo ELA!','ELA BOT: Sou uma inteligência artificial programada para aprender usando redes neurais. Sobre o que quer conversar? Use "::" no início da frase para falar comigo. Ex.: ":: Olá Ela!"'])
ultimo_texto = ''

while True:

    texto = bot.escuta()

    if texto != ultimo_texto and re.match(r'^::', texto):

        ultimo_texto = texto
        texto = texto.replace('::', '')
        texto = texto.lower()

        if (texto == 'aprender' or texto == ' aprender' or texto == 'ensinar' or texto == ' ensinar'):
            bot.aprender(texto,'ELA BOT: Oba! Eu adoro aprender e você pode me ajudar com isso. Escreva a pergunta e após o "?" escreva a resposta. Ex. "Qual a raiz quadrada de PI? 1.77245385091','ELA BOT: Que legal, adorei. Agora já sei!','ELA BOT: Acho que você escreveu algo errado! Comece novamente...')
        elif (texto == 'noticias' or texto == ' noticias' or texto == 'noticia' or texto == ' noticia' or texto == 'notícias' or texto == ' notícias' or texto == 'notícia' or texto == ' notícia'):
            bot.noticias()
        else:
            bot.responde(texto)
