from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
import sys
import json
sys.path.append('..')
from models_handler import ModelsHandler
from models import Organization, Department, OrgDepAssociation, Position, Employee, User
from waitress import serve


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd123'
bootstrap = Bootstrap(app)
db = ModelsHandler()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == int(user_id)).first()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=16)])
    remember = BooleanField('remember me')

    def get_user():
        return db.session.query(User).filter(User.username == LoginForm.username.data).first()

@app.route('/')
def index():
    models_handler = ModelsHandler()
    orgs = models_handler.get_organizations()
    models_handler.session.close()
    return render_template('index.html', orgs=orgs)

@app.route('/_get_org_phonebook')
def get_org_phonebook():
    models_handler = ModelsHandler()
    org = models_handler.get_organization_by_name(request.args.get('org', ''))
    org_deps = models_handler.get_org_deps_by_organization(org)
    phonebook = {'header': ['Отдел',
                            'Должность',
                            'ФИО',
                            'Номер телефона',
                            'Внутренний номер телефона',
                            'Электронная почта'],
                 'data': []}
    for org_dep in org_deps:
        dep = models_handler.get_department_by_id(org_dep.department_id)
        emps = models_handler.get_emps_by_org_dep(org_dep)
        emps = [{"full_name": str(emp),
                 "phone_number": emp.phone_number,
                 "internal_phone_number": emp.internal_phone_number,
                 "email": emp.email,
                 "position": models_handler.get_position_by_id(emp.position_id).title} for emp in emps]
        if emps:
            phonebook['data'].append({'dep': dep.title, 'emps': emps})

    models_handler.session.close()
    return Response(json.dumps(phonebook), mimetype='application/json')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user:
            if user.validate_password(form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin.index'))
        return 'Invlid username or password'
        # return '<h1>' + form.username.data + '</h1>'
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view=CustomAdminIndexView(), template_mode='bootstrap3')
admin.add_view(CustomModelView(Organization, db.session))
admin.add_view(CustomModelView(Department, db.session))
admin.add_view(CustomModelView(OrgDepAssociation, db.session))
admin.add_view(CustomModelView(Position, db.session))
admin.add_view(CustomModelView(Employee, db.session))
admin.add_view(CustomModelView(User, db.session))

if __name__ == '__main__':
    serve(app)
