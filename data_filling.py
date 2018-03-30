import models
import config
import random
from sqlalchemy.orm import sessionmaker


# models.Base.metadata.create_all(config.ENGINE)

session = sessionmaker(bind=config.ENGINE)()


organization_names = ['ОГБУ ЧРЦНИТ', 'МИТИС']
departments_titles = ['ПСИАС', 'Бухгалтерия', 'Администрация']
position_titles = ['Главный специалист', 'Начальник']
employee_names = ['Леонидова Яна Павеловна', 'Казакевича Изольда Давидовна',
                  'Смолина Антонина Игоревна', 'Клюев Глеб Агапович',
                  'Панюшкин ﻿Август Зиновиевич', 'Широнин Фома Иванович']

org_objs = []
for org in organization_names:
    org_objs.append(models.Organization(name=org))

session.add_all(org_objs)
session.flush()

dep_objs = []
for dep in departments_titles:
    dep_objs.append(models.Department(title=dep))

session.add_all(dep_objs)
session.flush()

pos_objs = []
for pos in position_titles:
    pos_objs.append(models.Position(title=pos))

session.add_all(pos_objs)
session.flush()
session.commit()

departments = session.query(models.Department).all()
department_ids = [dep.id for dep in departments]
positions = session.query(models.Position).all()
position_ids = [pos.id for pos in positions]
emp_objs = []
for emp in employee_names:
    emp_objs.append(models.Employee(surname=emp.split()[0],
                                    name=emp.split()[1],
                                    patronymic=emp.split()[2],
                                    phone_number=random.randint(100, 300),
                                    department_id=department_ids[random.randint(0, len(departments_titles))],
                                    position_id=position_ids[random.randint(0, len(position_titles))]))

session.add_all(emp_objs)
session.flush()

session.commit()