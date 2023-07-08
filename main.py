import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup
from datetime import datetime

bot = telebot.TeleBot("6272635544:AAHfs2PbPaHHBWuEVdDzrA7r-7U_fnGG3h4")

def get_currency_rates():
    response1 = requests.get("https://minfin.com.ua/ua/currency/usd/")
    soup1 = BeautifulSoup(response1.text, features="html.parser")
    usd_elements = soup1.find_all('div', {'class': "sc-1x32wa2-9 bKmKjX"})
    usd_values = [element.text.strip() for element in usd_elements]

    response2 = requests.get("https://minfin.com.ua/ua/currency/eur/")
    soup2 = BeautifulSoup(response2.text, features="html.parser")
    eur_elements = soup2.find_all('div', {'class': "sc-1x32wa2-9 bKmKjX"})
    eur_values = [element.text.strip() for element in eur_elements]

    response3 = requests.get("https://minfin.com.ua/ua/currency/pln/")
    soup3 = BeautifulSoup(response3.text, features="html.parser")
    pln_elements = soup3.find_all('div', {'class': "sc-1x32wa2-9 bKmKjX"})
    pln_values = [element.text.strip() for element in pln_elements]

    return usd_values, eur_values, pln_values

ukr_month_names = {
    1: "січня",
    2: "лютого",
    3: "березня",
    4: "квітня",
    5: "травня",
    6: "червня",
    7: "липня",
    8: "серпня",
    9: "вересня",
    10: "жовтня",
    11: "листопада",
    12: "грудня"
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Курс Долара")
    item2 = types.KeyboardButton("Курс Євро")
    item3 = types.KeyboardButton("Курс Злотих")
    markup.add(item1, item2, item3)

    current_date = datetime.now()
    ukr_month = ukr_month_names[current_date.month]
    ukr_date = current_date.strftime("%d") + " " + ukr_month + " " + current_date.strftime("%Y")

    bot.send_message(message.chat.id, "Яку валюту хочете дізнатися на стан {} року?".format(ukr_date), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.strip() == "Курс Долара":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Купівля")
        item2 = types.KeyboardButton("Продаж")
        item3 = types.KeyboardButton("Курс НБУ")
        markup.add(item1, item2, item3)

        usd_values, _, _ = get_currency_rates()
        answer = "Курс Долара:\n\nКупівля: {}\nПродаж: {}\nКурс НБУ: {}".format(usd_values[0], usd_values[1], usd_values[2])

    elif message.text.strip() == "Курс Євро":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Купівля")
        item2 = types.KeyboardButton("Продаж")
        item3 = types.KeyboardButton("Курс НБУ")
        markup.add(item1, item2, item3)

        _, eur_values, _ = get_currency_rates()
        answer = "Курс Євро:\n\nКупівля: {}\nПродаж: {}\nКурс НБУ: {}".format(eur_values[0], eur_values[1], eur_values[2])

    elif message.text.strip() == "Курс Злотих":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Купівля")
        item2 = types.KeyboardButton("Продаж")
        item3 = types.KeyboardButton("Курс НБУ")
        markup.add(item1, item2, item3)

        _, _, pln_values = get_currency_rates()
        answer = "Курс Злотих:\n\nКупівля: {}\nПродаж: {}\nКурс НБУ: {}".format(pln_values[0], pln_values[1], pln_values[2])

    else:
        answer = "Я не розумію вашого запиту."

    bot.send_message(message.chat.id, answer, reply_markup=markup)

bot.polling()
