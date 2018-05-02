import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

Base = declarative_base()

class OrgDepAssociation(Base):
    __tablename__ = 'org_dep_association'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    department_id = Column(Integer, ForeignKey('department.id'))
    employee = relationship("Employee")


class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    org_dep_association = relationship("OrgDepAssociation")
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Organization(name='%s')>" % self.name


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    # employee = relationship("Employee")
    org_dep_association = relationship("OrgDepAssociation")
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Department(title='%s')>" % self.title


class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    employee = relationship("Employee")
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Position(title='%s')>" % self.title


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    phone_number = Column(String)
    position_id = Column(Integer, ForeignKey('position.id'))
    org_dep_id = Column(Integer, ForeignKey('org_dep_association.id'))
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Employee(name='%s', surname='%s', patronymic='%s')>" % \
                (self.name, self.surname, self.patronymic)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String(300), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.encrypt(password)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        return "<User(username ='%s', password='%s')>" % \
                (self.username, self.password)

Base.metadata.create_all(config.ENGINE)
