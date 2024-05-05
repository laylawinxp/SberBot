from telebot import types, TeleBot
import config
from g4f.client import Client

bot = TeleBot(config.TOKEN)
global_messages = {}


def ask(content, msg_id):
    client = Client()
    if global_messages.get(msg_id, -1) == -1:
        global_messages[msg_id] = [{"role": "system",
                                    "content": config.prompt}]
    global_messages[msg_id].append({"role": "user", "content": content})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=global_messages[msg_id],
    )
    global_messages[msg_id].append(
        {"role": "assistant",
         "content": response.choices[0].message.content})
    return response.choices[0].message.content


@bot.message_handler(commands=['start'])
def on_start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Скачать приложение",
                                          url="http://www.sberbank.ru/ru/perso\
n/help/dist_services_inner_apps"))
    markup.add(
        types.InlineKeyboardButton("Веб-версия Сбера", url="http://www.sb\
erbank.ru/ru/person/dist_services/inner_sbol"))
    markup.add(types.InlineKeyboardButton("Курс валют",
                                          url="http://www.sberbank.ru/ru/quote\
s/currencies?tab=sbol&currency=BYN&currency=KZT&currency=EUR&currency=USD&pack\
age=ERNP-2"))
    markup.add(types.InlineKeyboardButton("Горячая линия",
                                          callback_data="call"))
    # bot.send_message(message.chat.id, "Привет! Я СберБот Фейерверк! Готов
    # ответить на Ваш вопрос :)")
    bot.reply_to(message, ask('Привет! Представься.', message.chat.id),
                 reply_markup=markup)


@bot.message_handler(commands=['clear'])
def on_clear(message):
    global_messages[message.chat.id] = [{"role": "system",
                                         "content": config.prompt}]
    bot.reply_to(message, "Контекст был очищен.")


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "call":
        number = "С мобильного телефона в России: `900`\nС мобильного или горо\
дского из-за границы:\n`+7 495 500-55-50`"
        bot.send_message(callback.message.chat.id,
                         number, parse_mode="MARKDOWN")


@bot.message_handler(func=lambda message: True)
def on_message(message):
    bot.reply_to(message, ask(message.text, message.chat.id))


bot.polling(none_stop=True)
