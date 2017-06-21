# -*- coding:utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import flask_login
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from flask_mail import Mail

#from application.reglogin import reglogin

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.secret_key = 'instagram'

#app.register_blueprint(reglogin, url_prefix='/reglogin')

db = SQLAlchemy(app)
login_manager = flask_login.LoginManager(app)
login_manager.login_view = '/wtf/login/'

bootstrap = Bootstrap(app)

mail = Mail(app)

from application import models, views
