# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import config
import models
import redis_manager
import morph_analyzer
import telebot
import os
import numpy as np
import logging
from platform import system as system_name
from os import system as system_call
from models_handler import ModelsHandler
import re
from telebot import apihelper


logging.basicConfig(filename='bot.log', level=logging.INFO)
apihelper.proxy = {'https':'socks5://47.75.31.98:1080'}
models_handler = ModelsHandler()
bot = telebot.TeleBot(config.TOKEN)

def ping(host):
    parameters = "-n 1" if system_name().lower() == "windows" else "-c 1"
    return system_call("ping " + parameters + " " + host) == 0

def get_phone_book(org_dep_id=None):
    if org_dep_id:
        employees = models_handler.get_employees_by_org_dep_id(org_dep_id)
    else:
        employees = models_handler.get_employees()
    phone_book = ""
    for emp in employees:
        phone_book += get_employee_info(emp)
    return phone_book

def get_org_keyboard(organization_names):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for org in organization_names:
        keyboard.add(telebot.types.InlineKeyboardButton(text=org, callback_data=org))
    return keyboard

def get_employee_info(obj):
    return obj.name + " " \
           + obj.surname + " " \
           + obj.patronymic + "\t" \
           + str(obj.phone_number) + "\n"

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 
                     "Список доступных команд:\
                     \n/phone - телефон сотрудника (поиск по фамилии, имени)\
                     \n/phonebook - телефонный справочник")

@bot.message_handler(commands=['ping'])
def handle_ping(message):
    pass

@bot.message_handler(commands=['phone'])
def phone(message):
    text = re.sub('/phone', '', message.text).strip()
    if text:
        employees = models_handler.get_employees()
        emp_rates = []
        for emp in employees:
            emp_rates.append(morph_analyzer.string_detection(emp.name + " " + emp.surname, text))
        nearest = [idx for idx in np.argsort(emp_rates) if np.array(emp_rates)[idx] > config.HIGH_RATE_EMPLOYEEE]
        if nearest:
            for n in nearest:
                bot.send_message(message.chat.id, get_employee_info(employees[n]))
        else:
            indexes = np.argsort(emp_rates)[-3:]
            similar_exists = False
            for r in np.array(emp_rates)[indexes]:
                if r > config.AVERAGE_RATE_EMPLOYEEE:
                    similar_exists = True
            if similar_exists and len(text) > 3:
                bot.send_message(message.chat.id, "Наиболее подходящие контакты:")
                for n in indexes:
                    bot.send_message(message.chat.id, get_employee_info(employees[n]))
            else:
                bot.send_message(message.chat.id, "Нет подходящих контактов")

@bot.message_handler(commands=['phonebook'])
def phone_book(message):
    if message != '':
        phone_book = get_phone_book()
    organization_names = [org.name for org in models_handler.get_organizations()]
    keyboard = get_org_keyboard(organization_names)
    bot.send_message(message.chat.id, "Выберите организацию", reply_markup=keyboard)
    redis_manager.set_state(message.chat.id, 'phonebook')

def phonebook_handler(bot, message, organization_names):
    keyboard = get_org_keyboard(organization_names)
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text="Выберите организацию",
                          reply_markup=keyboard)
    redis_manager.set_state(message.chat.id, 'phonebook')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        organizations = models_handler.get_organizations()
        departments = models_handler.get_departments()
        organization_names = [org.name for org in organizations]
        department_ids = [dep.id for dep in departments]
        if call.data == 'phonebook':
            phonebook_handler(bot, call.message, organization_names)
        elif call.data in organization_names:
            previous_state = redis_manager.get_current_state(call.message.chat.id)
            redis_manager.set_state(call.message.chat.id, call.data)
            call_org = models_handler.get_organization_by_name(call.data)
            keyboard = telebot.types.InlineKeyboardMarkup()
            dep_by_org = models_handler.get_departments_by_organization(call_org)
            for dep in departments:
                if dep.title in [x.title for x in dep_by_org]:
                    org_dep = models_handler.get_org_dep(call_org, dep)
                    keyboard.add(telebot.types.InlineKeyboardButton(text=dep.title,
                                                                    callback_data=config.DEPARTMENT_CODENAME + str(org_dep.id)))
            keyboard.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data=previous_state))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Выберите отдел",
                                  reply_markup=keyboard)
        elif config.DEPARTMENT_CODENAME in call.data:
            org_dep_id = int(call.data[len(config.DEPARTMENT_CODENAME):])
            if org_dep_id in department_ids:
                previous_state = redis_manager.get_current_state(call.message.chat.id)
                redis_manager.set_state(call.message.chat.id, call.data)
                text = get_phone_book(org_dep_id)
                if not text:
                    text = 'Список сотрудников пуст'
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=text)
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception:
        logging.warning(Exception)
