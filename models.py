import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from flask_login import UserMixin
from sqlalchemy import event

Base = declarative_base()

class OrgDepAssociation(Base):
    __tablename__ = 'org_dep_association'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    department_id = Column(Integer, ForeignKey('department.id'))
    organization = relationship("Organization")
    department = relationship("Department")

    def __str__(self):
        return "{} - {}".format(self.organization, self.department)


class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return "<Organization(name='%s')>" % self.name

    def __str__(self):
        return self.name


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Department(title='%s')>" % self.title

    def __str__(self):
        return self.title


class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Position(title='%s')>" % self.title

    def __str__(self):
        return self.title


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone_number = Column(String)
    internal_phone_number = Column(String)
    email = Column(String)
    position_id = Column(Integer, ForeignKey('position.id'))
    org_dep_id = Column(Integer, ForeignKey('org_dep_association.id'))
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())
    org_dep_association = relationship("OrgDepAssociation")
    position = relationship("Position")

    def __repr__(self):
        return "<Employee(name='%s', surname='%s', patronymic='%s')>" % \
                (self.name, self.surname, self.patronymic)

    def __str__(self):
        return "%s %s %s" % (self.surname, self.name, self.patronymic)


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String(300), nullable=False)

    # def __init__(self, username, password):
    #     self.username = username
    #     self.password = bcrypt.encrypt(password)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return "<User(username ='%s', password='%s')>" % \
                (self.username, self.password)


@event.listens_for(User, 'before_insert')
def receive_before_insert(mapper, connection, target):
    target.password = bcrypt.encrypt(target.password)

@event.listens_for(User, 'before_update')
def receive_before_update(mapper, connection, target):
    target.password = bcrypt.encrypt(target.password)

Base.metadata.create_all(config.ENGINE)
