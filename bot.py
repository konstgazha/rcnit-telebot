# -*- coding: utf-8 -*-
import config
import telebot
import os
from platform import system as system_name
from os import system as system_call

bot = telebot.TeleBot(config.TOKEN)

def ping(host):
    parameters = "-n 1" if system_name().lower() == "windows" else "-c 1"
    return system_call("ping " + parameters + " " + host) == 0

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 
                     """Список доступных команд:\n
                     /ping - статус серверов""")

@bot.message_handler(commands=['ping'])
def handle_pinf(message):
    pass

if __name__ == '__main__':
    bot.polling(none_stop=True)