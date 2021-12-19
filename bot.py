import telebot
import config
from config import *
import urllib
import time
from tensorflow import keras
from neural import img_to_str

bot = telebot.TeleBot(config.TOKEN)
model = keras.models.load_model('text_writer_model.h5')

def tel_bot(TOKEN):


    @bot.message_handler(commands=['start'])
    def welcome(message):
        bot.send_message(message.chat.id, 'Считывание текста с картинки')


   #

    @bot.message_handler(content_types=['photo'])
    def handle_docs_photo(message):

        try:

            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'D:/pythonProject/botik/' + file_info.file_path;
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Фото добавлено")
            result = img_to_str(model, src)
            print(result)
            bot.send_message(message.chat.id, f"{result}")
        except Exception as e:
            bot.reply_to(message, e)


#D:/pythonProject/botik

if __name__ == "__main__":
    try:
        tel_bot(TOKEN)
        bot.polling(none_stop=True)  # запуск бота
    except Exception as e:
        print(e)  # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)