# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from enum import Enum

TOKEN = ''

SERVERS = ["sd.gov74.ru", "op-mon.pravmin74.ru", "sc.gov74.ru"]


DATABASE_NAME = 'rcnit_telebot'
DATABASE_HOST = 'localhost'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'admin'
DATABASE_ENGINE = 'postgresql+psycopg2'
ENGINE = create_engine('{0}://{1}:{2}@{3}/{4}'.format(DATABASE_ENGINE,
                                                      DATABASE_USER,
                                                      DATABASE_PASSWORD,
                                                      DATABASE_HOST,
                                                      DATABASE_NAME))

DEPARTMENT_CODENAME = 'dep'


class States(Enum):
    PHONEBOOK_START = "0"
    PHONEBOOK_ORGANIZATION = "1"
    PHONEBOOK_DEPARTMENT = "2"
    PHONEBOOK_EMPLOYEE = "3"
