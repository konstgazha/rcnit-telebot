# -*- coding: utf-8 -*-
import config
import models
import morph_analyzer
import redis_manager
import telebot
import os
import numpy as np
from platform import system as system_name
from os import system as system_call
from sqlalchemy.orm import sessionmaker
import re

session = sessionmaker(bind=config.ENGINE)()
bot = telebot.TeleBot(config.TOKEN)

def ping(host):
    parameters = "-n 1" if system_name().lower() == "windows" else "-c 1"
    return system_call("ping " + parameters + " " + host) == 0

def get_organizations():
    return session.query(models.Organization).all()

def get_departments():
    return session.query(models.Department).all()

def get_employees():
    return session.query(models.Employee).all()

def get_organization_by_name(name):
    return session.query(models.Organization).\
                   filter(models.Organization.name == name)

def get_org_dep_by_id(_id):
    return session.query(models.OrgDepAssociation).\
                   filter(models.OrgDepAssociation.id == _id)

def get_org_dep(organization, department):
    return session.query(models.OrgDepAssociation).\
                   filter(models.OrgDepAssociation.organization_id == organization.id,
                          models.OrgDepAssociation.department_id == department.id).first()

def get_departments_by_organization(organization):
    org_deps = session.query(models.OrgDepAssociation).\
                       filter(models.OrgDepAssociation.organization_id == organization.id).all()
    departments = []
    for org_dep in org_deps:
        departments.append(session.query(models.Department).\
                                   filter(models.Department.id == org_dep.department_id).first())
    return departments

def get_department_by_id(id):
    return session.query(models.Department).\
                   filter(models.Department.id == id)

def get_phone_book(org_dep_id=None):
    if org_dep_id:
        employees = session.query(models.Employee).\
                            filter(models.Employee.org_dep_id == org_dep_id)
    else:
        employees = session.query(models.Employee).all()
    phone_book = ""
    for emp in employees:
        phone_book += "{0} {1} {2} {3}\n".format(emp.name,
                                                 emp.surname,
                                                 emp.patronymic,
                                                 emp.phone_number)
    return phone_book

def get_org_keyboard(organization_names):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for org in organization_names:
        keyboard.add(telebot.types.InlineKeyboardButton(text=org, callback_data=org))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 
                     """Список доступных команд:
    /ping - статус серверов
    /phone - телефон сотрудника
    /phonebook - телефонный справочник""")

@bot.message_handler(commands=['ping'])
def handle_ping(message):
    pass

@bot.message_handler(commands=['phone'])
def phone(message):
    text = re.sub('/phone', '', message.text).strip()
    if text:
        employees = get_employees()
        emp_rates = []
        for emp in employees:
            emp_rates.append(morph_analyzer.string_detection(emp.name + " " + emp.surname, text))
        top_rated = np.argsort(emp_rates)[-3:]
        for n in top_rated:
            if emp_rates[n] > 0.6:
                bot.send_message(message.chat.id, employees[n].name + " "
                                 + employees[n].surname + " "
                                 + employees[n].patronymic + " "
                                 + str(employees[n].phone_number))
                break
        # bot.send_message(message.chat.id, "Нет подходящих контактов")

@bot.message_handler(commands=['phonebook'])
def phone_book(message):
    if message != '':
        phone_book = get_phone_book()
    organization_names = [org.name for org in get_organizations()]
    keyboard = get_org_keyboard(organization_names)
    bot.send_message(message.chat.id, "Выберите организацию", reply_markup=keyboard)
    redis_manager.set_state(message.chat.id, 'phonebook')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        organizations = get_organizations()
        departments = get_departments()
        organization_names = [org.name for org in organizations]
        department_ids = [dep.id for dep in departments]
        if call.data == 'phonebook':
            keyboard = get_org_keyboard(organization_names)
            bot.edit_message_text(chat_id=call.message.chat.id,
                      message_id=call.message.message_id,
                      text="Выберите организацию",
                      reply_markup=keyboard)
            redis_manager.set_state(call.message.chat.id, 'phonebook')
        elif call.data in organization_names:
            previous_state = redis_manager.get_current_state(call.message.chat.id)
            redis_manager.set_state(call.message.chat.id, call.data)
            call_org = get_organization_by_name(call.data).first()
            keyboard = telebot.types.InlineKeyboardMarkup()
            dep_by_org = get_departments_by_organization(call_org)
            for dep in departments:
                if dep.title in [x.title for x in dep_by_org]:
                    org_dep = get_org_dep(call_org, dep)
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
                # dep_org = get_org_dep_by_id(org_dep_id)
                # department = get_department_by_id(dep_org.id).first()
                text = get_phone_book(org_dep_id)
                if not text:
                    text = 'Список сотрудников пуст'
                # keyboard.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data=previous_state))
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=text)
if __name__ == '__main__':
    bot.polling(none_stop=True)