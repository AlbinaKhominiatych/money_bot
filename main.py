import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup
from datetime import datetime

bot = telebot.TeleBot("6272635544:AAHfs2PbPaHHBWuEVdDzrA7r-7U_fnGG3h4")

def get_currency_rates():
    response1 = requests.get("https://minfin.com.ua/ua/currency/usd/")
    soup1 = BeautifulSoup(response1.text, features="html.parser")
    for usd_rate in soup1.find('div', {'class': "sc-1x32wa2-9 bKmKjX"}):
        usd_rate.extract()


    response2 = requests.get("https://minfin.com.ua/ua/currency/eur/")
    soup2 = BeautifulSoup(response2.text, features="html.parser")
    for eur_rate in soup2.find('div', {'class': "sc-1x32wa2-9 bKmKjX"}):
        eur_rate.extract()

    response3 = requests.get("https://minfin.com.ua/ua/currency/pln/")
    soup3 = BeautifulSoup(response3.text, features="html.parser")
    for pln_rate in soup3.find('div', {'class': "sc-1x32wa2-9 bKmKjX"}):
        pln_rate.extract()

    return usd_rate, eur_rate, pln_rate

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
        usd_rate, _, _ = get_currency_rates()
        answer = "Курс Долара становить {}".format(usd_rate)
    elif message.text.strip() == "Курс Євро":
        _, eur_rate, _ = get_currency_rates()
        answer = "Курс Євро становить {}".format(eur_rate)
    elif message.text.strip() == "Курс Злотих":
        _, _, pln_rate = get_currency_rates()
        answer = "Курс Злотих становить {}".format(pln_rate)
    else:
        answer = "Я не розумію вашого запиту."

    bot.send_message(message.chat.id, answer)

bot.polling()
