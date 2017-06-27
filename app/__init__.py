# -*- coding: UTF-8 -*-   
from flask import Flask,abort
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES,configure_uploads,ALL
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin,AdminIndexView,expose
from config import config
from flask_login import login_required,current_user
bootstrap=Bootstrap()
moment=Moment()
db=SQLAlchemy()

class MyHomeView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if current_user.is_admin():
            return self.render('admin/index.html')
        else:
            abort(404)

admin=Admin(name=u'if',index_view=MyHomeView())
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'

pictures=UploadSet('pictures',IMAGES)


def create_app(config_name):
    app=Flask(__name__,static_url_path='/static')
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    configure_uploads(app,pictures)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint)

    return app
