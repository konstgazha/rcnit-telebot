import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Organization(name='%s')>" % self.name


class Department(models.Model):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Department(title='%s')>" % self.title


class Position(models.Model):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    title = Column(String)
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
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Employee(name='%s', surname='%s', patronymic='%s')>" % (
                self.name, self.surname, self.patronymic)

Employee.__table__
Base.metadata.create_all(config.ENGINE)
