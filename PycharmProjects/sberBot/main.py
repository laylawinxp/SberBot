import requests
import telebot
from telebot import types
import config
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def on_start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Скачать приложение",
                                          url="http://www.sberbank.ru/ru/person/help/dist_services_inner_apps"))
    markup.add(
        types.InlineKeyboardButton("Веб-версия Сбера", url="http://www.sberbank.ru/ru/person/dist_services/inner_sbol"))
    markup.add(types.InlineKeyboardButton("Курс валют",
                                          url="http://www.sberbank.ru/ru/quotes/currencies?tab=sbol&currency=BYN&currency=KZT&currency=EUR&currency=USD&package=ERNP-2"))
    markup.add(types.InlineKeyboardButton("Горячая линия", callback_data="call"))
    # bot.send_message(message.chat.id, "Привет! Я СберБот Фейерверк! Готов ответить на Ваш вопрос :)")
    bot.reply_to(message, "Привет! Я СберБот Фейерверк! Готов ответить на Ваш вопрос :)", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "call":
        number = "С мобильного телефона в России: `900`\nС мобильного или городского из-за границы:\n`+7 495 500-55-50`"
        bot.send_message(callback.message.chat.id, number, parse_mode="MARKDOWN")


@bot.message_handler()
def text_handler(message):
    ...


bot.polling(none_stop=True)
