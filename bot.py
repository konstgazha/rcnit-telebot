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

def get_departments():
    return session.query(models.Department).all()

def get_organization_by_name(name):
    return session.query(models.Organization).\
                   filter(models.Organization.name == name)

def get_departments_by_organization(organization):
    return session.query(models.Department).\
                   filter(models.Department.organization.any(id=organization.id))

def get_department_by_id(id):
    return session.query(models.Department).\
                   filter(models.Department.id == id)

def get_phone_book(department=None):
    if department:
        employees = session.query(models.Employee).\
                            filter(models.Employee.department_id == department.id)
    else:
        employees = session.query(models.Employee).all()
    phone_book = ""
    for emp in employees:
        phone_book += "{0} {1} {2}\n".format(emp.name,
                                             emp.surname,
                                             emp.patronymic)
    return phone_book

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
    if message != '':
        phone_book = get_phone_book()
    organizations = [org.name for org in get_organizations()]
    keyboard = telebot.types.InlineKeyboardMarkup()
    for org in organizations:
        keyboard.add(telebot.types.InlineKeyboardButton(text=org, callback_data=org))
    bot.send_message(message.chat.id, "Выберите организацию", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        organizations = get_organizations()
        departments = get_departments()
        organization_names = [org.name for org in organizations]
        department_ids = [dep.id for dep in departments]
        if call.data in organization_names:
            call_org = get_organization_by_name(call.data).first()
            keyboard = telebot.types.InlineKeyboardMarkup()
            dep_by_org = get_departments_by_organization(call_org).all()
            for dep in departments:
                if dep.title in [x.title for x in dep_by_org]:
                    keyboard.add(telebot.types.InlineKeyboardButton(text=dep.title,
                                                                    callback_data=config.DEPARTMENT_CODENAME + str(dep.id)))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Выберите отдел",
                                  reply_markup=keyboard)
        if config.DEPARTMENT_CODENAME in call.data:
            dep_id = int(call.data[len(config.DEPARTMENT_CODENAME):])
            if dep_id in department_ids:
                department = get_department_by_id(dep_id).first()
                text = get_phone_book(department)
                if not text:
                    text = 'Список сотрудников пуст'
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=text)
if __name__ == '__main__':
    bot.polling(none_stop=True)