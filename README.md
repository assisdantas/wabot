# WABOT
WhatsApp Bot with Python and Selenium 

Baseado no projeto original, encontrado em:
https://github.com/jonathanferreiras/whats-bot

Algumas implementações feitas.


### Requerimentos

Para utilizar, utilize Python 3.x. 
Utilize a ferramenta pip3 para instalar as bibliotecas, caso não tenha, utilize o comando:

Linux Terminal:
> apt install python3-pip

Instale os requerimentos utilizando o Pip3:
>pip3 install setuptools chatterbot chatterbot-corpus selenium


### Uso

Antes de utilizar é necessário editar os arquivos 'bot.py' e 'main.py' faça as alterações conforme necessário nos seguintes trechos:

#### Editando 'main.py'

Linhas 6 e 8 (main.py):

```python
bot = wppbot('nome_do_bot') # Nome do bot
[...]
bot.inicia('grupo_wapp') # Grupo que o bot irá entrar
```

#### Setando o WebDriver

Baixe o Chrome Web Driver para a versão do seu navegador.

[https://chromedriver.chromium.org/downloads]

Salve o arquivo baixado na mesma pasta do "main.py".

#### Rodando o Bot

Para rodar o Bot basta abrir o terminal na pasta dos arquivos e utilizar o comando:

>python3 main.py

Leia o código QR utilizando a conta do WhatsApp.

Para responder ao Bot, utlize "::" na frente das mensagens. Ex.: ":: qual seu nome?"

#### Treinamento

Para dar uma referência de dados ao Bot para treinamento, vá para "/treino/treino.txt" e edite a lista de perguntas e respostas.
