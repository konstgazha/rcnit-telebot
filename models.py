import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
# organization_department_association = Table('organization_department', Base.metadata,
#     Column('organization_id', Integer, ForeignKey('organization.id')),
#     Column('department_id', Integer, ForeignKey('department.id'))
# )
class OrgDepAssociation(Base):
    __tablename__ = 'org_dep_association'
    id = Column(Integer, primary_key=True, unique=True)
    org_id = Column(Integer, ForeignKey('organization.id'), primary_key=True)
    dep_id = Column(Integer, ForeignKey('department.id'), primary_key=True)
    employee = relationship("Employee")
    # employee = relationship("Employee", secondary='employee')


class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = relationship("Department", secondary='org_dep_association')
    # department = relationship("Department", back_populates="organization")
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Organization(name='%s')>" % self.name


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    employee = relationship("Employee")
    organization = relationship("Organization", secondary='org_dep_association')
    # organization = relationship("Organization", back_populates="department")
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
        return "<Employee(name='%s', surname='%s', patronymic='%s')>" % (
                self.name, self.surname, self.patronymic)


Base.metadata.create_all(config.ENGINE)
