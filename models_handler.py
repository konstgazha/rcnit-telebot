import models
import config
from sqlalchemy.orm import sessionmaker

class ModelsHandler:
    def __init__(self):
        self.session = sessionmaker(bind=config.ENGINE)()

    def get_organizations(self):
        return self.session.query(models.Organization).all()

    def get_departments(self):
        return self.session.query(models.Department).all()

    def get_employees(self):
        return self.session.query(models.Employee).all()

    def get_employees_by_org_dep_id(self, org_dep_id):
        return self.session.query(models.Employee).\
                            filter(models.Employee.org_dep_id == org_dep_id)

    def get_organization_by_name(self, name):
        return self.session.query(models.Organization).\
                            filter(models.Organization.name == name).first()

    def get_org_dep_by_id(self, _id):
        return self.session.query(models.OrgDepAssociation).\
                            filter(models.OrgDepAssociation.id == _id)

    def get_org_dep(self, organization, department):
        return self.session.query(models.OrgDepAssociation).\
                            filter(models.OrgDepAssociation.organization_id == organization.id,
                                   models.OrgDepAssociation.department_id == department.id).first()

    def get_departments_by_organization(self, organization):
        org_deps = self.session.query(models.OrgDepAssociation).\
                                filter(models.OrgDepAssociation.organization_id == organization.id).all()
        departments = []
        for org_dep in org_deps:
            departments.append(self.session.query(models.Department).\
                                            filter(models.Department.id == org_dep.department_id).first())
        return departments

    def get_department_by_id(self, _id):
        return self.session.query(models.Department).\
                            filter(models.Department.id == _id)

    def get_organization_by_id(self, _id):
        return self.session.query(models.Organization).\
                            filter(models.Organization.id == _id)