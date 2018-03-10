# -*- coding: utf-8 -*-
import config
import models
import morph_analyzer
import telebot
import os
from platform import system as system_name
from os import system as system_call
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=config.ENGINE)()
bot = telebot.TeleBot(config.TOKEN)

def ping(host):
    parameters = "-n 1" if system_name().lower() == "windows" else "-c 1"
    return system_call("ping " + parameters + " " + host) == 0

def get_organizations():
    return session.query(models.Organization).all()

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 
                     """Список доступных команд:
    /ping - статус серверов
    /phone - телефонный справочник""")

@bot.message_handler(commands=['ping'])
def handle_ping(message):
    pass

@bot.message_handler(commands=['phone'])
def phone_book(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    organizations = [org.name for org in get_organizations()]
    for org in organizations:
        keyboard.add(telebot.types.InlineKeyboardButton(text=org, callback_data=org))
    bot.send_message(message.chat.id, "Выберите организацию", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    organizations = [org.name for org in get_organizations()]
    if call.message:
        if call.data in organizations:
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text="Выберите отдел")

if __name__ == '__main__':
    bot.polling(none_stop=True)