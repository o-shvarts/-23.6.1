import telebot
from extensions import ConvertionException, Exceptions
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы получить список доступных валют введите команду /values. \nВведите команду /start или /help для " \
           "получения информации.\"" \
           "Чтобы начать работу введите команду в следующем формате: \<название валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты>"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) == 3:    #Немного изменил конструкцию
            base, quote, amount = values

            total_quote = Exceptions.get_price(base, quote, amount)
            amount = float(amount)

            text = f'Стоимость {amount} {base} - {(total_quote * amount)} {quote}'
        else:
            text = 'В Вашем сообщении должно быть три параметра написанных через пробел: валюта, которую необходимо ' \
                   'конвертировать, валюта для конвертации и количество конвертируемой валюты '
    except ConvertionException as e:
        text = f'Произошла ошибка. \n {e}'
    except Exception as e:
        text = 'Произошла непредвиденная ошибка'


    bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
