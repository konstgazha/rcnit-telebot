from flask import Flask, jsonify, render_template, request, Response
import sys
import json
sys.path.append('..')
from models_handler import ModelsHandler

app = Flask(__name__)

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
    phonebook = []
    for org_dep in org_deps:
        dep = models_handler.get_department_by_id(org_dep.department_id)
        emps = models_handler.get_emps_by_org_dep(org_dep)
        emps = [{"name": emp.name,
                 "surname": emp.surname,
                 "patronymic": emp.patronymic,
                 "phone_number": emp.phone_number,
                 "position": models_handler.get_position_by_id(emp.position_id).title} for emp in emps]
        phonebook.append({'dep': dep.title, 'emps': emps})

    models_handler.session.close()
    # print(phonebook)
    # print(jsonify(phonebook))
    return Response(json.dumps(phonebook), mimetype='application/json')