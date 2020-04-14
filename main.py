import telebot
import flask
import requests
import os.path

token = '1109064489:AAHovWSdEB0uLmGXLjkUpzrVslwXU2hlKpY'
app_name = 'translator-bot1'

server = flask.Flask('__name__')
bot = telebot.TeleBot(token)#подключаем файл к телеграм боту

@bot.message_handler(commands=['start'])#реагирует на команду старт, обработчик
def start(message):
     msg = bot.send_message(message.chat.id, 'Hey, write me something')#бот отправляет сообщение


@server.route('/' + token, methods=['POST'])
def get_message():
     bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
     return "!", 200

@server.route('/', methods=["GET"])
def index():
     print("hello webhook!")
     bot.remove_webhook()
     bot.set_webhook(url=f"https://{app_name}.herokuapp.com/{token}")
     return "Hello from Heroku!", 200
     
print(f"https://{app_name}.herokuapp.com/{token}")
print(f"PORT: {int(os.environ.get('PORT', 5000))}")
if __name__ == '__main__':
     print("started")
     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))    
#bot.polling(none_stop=True)#запускаем поллинг, т.е. цикл
