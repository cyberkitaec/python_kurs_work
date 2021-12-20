import telebot
import config
from config import *
import urllib
import time
from tensorflow import keras
from neural import img_to_str
import digit
from digit import cnn_digits_predict
import sqlite3 as sq
con = sq.connect("log.db", check_same_thread=False)
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users (date TEXT, message TEXT)""")

bot = telebot.TeleBot(config.TOKEN)
model = keras.models.load_model('text_writer_model.h5')
model_digit = keras.models.load_model('cnn_digits_28x28.h5')


def tel_bot(TOKEN):
    @bot.message_handler(commands=['start'])
    def welcome(message):
        bot.send_message(message.chat.id, 'Считывание текста с картинки')

    @bot.message_handler(commands=['photo'])
    def command_photo(message):
        bot.send_message(message.chat.id, "Отправте фотографию")

        @bot.message_handler(content_types=['photo'])
        def handle_docs_photo(message):

            try:

                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = 'D:/pythonProject/neural_ocr/' + file_info.file_path;
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.send_message(message.chat.id, "Фото добавлено")
                result = img_to_str(model, src)
                print(result)
                bot.send_message(message.chat.id, f"{result}")
                cur.execute("INSERT INTO users(date, message) VALUES(date('now'), ?)", result[0])
            except Exception as e:
                cur.execute("INSERT INTO users(date, message) VALUES(date('now'), ?)", e)


    @bot.message_handler(commands=['digit'])
    def command_digit(message):
        bot.send_message(message.chat.id, "Считывание цифр с фото")

        @bot.message_handler(content_types=['photo'])
        def handle_digit_photo(message):
            try:

                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = 'D:/pythonProject/neural_ocr/' + file_info.file_path;
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.send_message(message.chat.id, "Фото добавлено")
                result = cnn_digits_predict(model_digit, src)
                print(result)
                bot.send_message(message.chat.id, f"{result}")
                cur.execute("INSERT INTO users(date, message) VALUES(date('now'), ?)", result[0])
            except Exception as e:
                cur.execute("INSERT INTO users(date, message) VALUES(date('now'), ?)", e)


if __name__ == "__main__":
    try:
        tel_bot(TOKEN)
        bot.polling(none_stop=True)
    except Exception as e:
        cur.execute("INSERT INTO users(date, message) VALUES(date('now'), ?)", e)
        time.sleep(15)