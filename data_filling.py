import models
import config
from sqlalchemy.orm import sessionmaker


# models.Base.metadata.create_all(config.ENGINE)

session = sessionmaker(bind=config.ENGINE)()


organization_names = ['ОГБУ ЧРЦНИТ', 'МИТИС']
departments_titles = ['ПСИАС', 'Бухгалтерия', 'Администрация']


org_objs = []
for org in organization_names:
    org_objs.append(models.Organization(name=org))

dep_objs = []
for dep in departments_titles:
    dep_objs.append(models.Department(title=dep))

session.add_all(org_objs)
session.flush()

session.add_all(dep_objs)
session.flush()

session.commit()