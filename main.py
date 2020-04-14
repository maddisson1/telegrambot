import telebot
from telebot import types
import config
import flask
import requests
import os.path

bot = telebot.TeleBot(config.token)#подключаем файл к телеграм боту
server = flask.Flask(__name__)

@bot.message_handler(commands=['start'])#реагирует на команду старт, обработчик
def start(message):
     msg = bot.send_message(message.chat.id, 'Hey, write me something')#бот отправляет сообщение


@server.route('/' + config.token, methods=['POST'])
def get_message():
     bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
     return "!", 200

@server.route('/', methods=["GET"])
def index():
     print("hello webhook!")
     bot.remove_webhook()
     bot.set_webhook(url=f"https://{config.app_name}.herokuapp.com/{config.token}")
     return "Hello from Heroku!", 200
     
print(f"https://{config.app_name}.herokuapp.com/{config.token}")
print(f"PORT: {int(os.environ.get('PORT', 5000))}")
if __name__ == '__main__':
     print("started")
     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))    
#bot.polling(none_stop=True)#запускаем поллинг, т.е. цикл
