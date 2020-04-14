import telebot #библиотека для создания ботов
from telebot import types #модуль, отвечающий за клавиатуру
from gtts import gTTS #библиотека, помогающая воспроизводить текст
from googletrans import Translator #библиотека, позволяющая переводить текст
import flask
import os

token = '1109064489:AAHovWSdEB0uLmGXLjkUpzrVslwXU2hlKpY'

bot = telebot.TeleBot(token)#подключаем файл к телеграм боту
server = flask.Flask(__name__)
@bot.message_handler(commands=['start'])#реагирует на команду старт, обработчик
def start(message):
     msg = bot.send_message(message.chat.id, 'Hey, write me something')#бот отправляет сообщение
     bot.register_next_step_handler(msg, voice)#переход на следующую функцию
     
@bot.message_handler(content_types=['text'])#реагирует на текст
def voice(message):
     text = message.text #сохраняем текст от пользователя в переменную text
     translator = Translator()#запускаем переводчик
     trans = translator.translate(text, dest='ru')#переводим введенный текст на русский
     speech = gTTS(trans.text, 'ru', slow=False)#преобразовываем переведенный текст в аудио
     speech.save('translatedtext.mp3')#сохраняем локально, на компьютере
     sp = open('translatedtext.mp3', 'rb')#открываем аудио файл в режиме считывания
     bot.send_audio(message.chat.id, sp)#отправляем пользователю

@server.route('/' + token, methods=['POST'])
def get_message():
     bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
     return "!", 200

@server.route('/', methods=["GET"])
def index():
     print("hello webhook!")
     bot.remove_webhook()
     bot.set_webhook(url=f"https://{APP_NAME}.herokuapp.com/{token}")
     return "Hello from Heroku!", 200
     
print(f"https://{APP_NAME}.herokuapp.com/{token}")
print(f"PORT: {int(os.environ.get('PORT', 5000))}")
if __name__ == "__main__":
     print("started")
     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))    
#bot.polling(none_stop=True)#запускаем поллинг, т.е. цикл
