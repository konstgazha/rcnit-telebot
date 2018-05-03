from flask import Flask
from flask import render_template
import sys
sys.path.append('../bot')
from sqlalchemy.orm import sessionmaker
import models, config

app = Flask(__name__)

@app.route('/')
def index():
    session = sessionmaker(bind=config.ENGINE)()
    orgs = [org.name for org in session.query(models.Organization).all()]
    return render_template('index.html', orgs=orgs)
