import telebot
from config import TOKEN, KEYS
import extensions



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    bot.reply_to(message, "Посмотреть доступные валюты: /values \n"
                          "Как сделать запрос боту: /request")

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = ""
    for key in KEYS:
        text += key + "\n"

    bot.reply_to(message, text)

@bot.message_handler(commands=["request"])
def request(message: telebot.types.Message):
    bot.reply_to(message, "Введите:\n"
                          "<Имя валюты>, <Имя валюты в которую хотите перевести>, <Количество>\n"
                          "Пример\n"
                          "доллар рубль 1")



@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    valuers = message.text.split(" ")


    result = extensions.CurrencyConverted.get_price(valuers)


    bot.reply_to(message, result)


def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()


