# -*- coding: UTF-8 -*-   
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES,configure_uploads,ALL
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap=Bootstrap()
moment=Moment()
db=SQLAlchemy()

login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'

pictures=UploadSet('pictures',IMAGES)


def create_app(config_name):
    app=Flask(__name__,static_url_path='/static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    configure_uploads(app,pictures)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    return app
