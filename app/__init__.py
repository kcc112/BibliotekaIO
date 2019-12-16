from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)

    
    from .books_app import books_app as books_app_blueprint
    app.register_blueprint(books_app_blueprint)

    from .announcements_app import announcements_app as announcements_app_blueprint
    app.register_blueprint(announcements_app_blueprint)

    from .main_app import main_app as main_app_blueprint
    app.register_blueprint(main_app_blueprint)

    from .registration_login_app import registration_login_app as registration_login_app_blueprint
    app.register_blueprint(registration_login_app_blueprint)
    
    from .owner_app import owner_app as owner_app_blueprint
    app.register_blueprint(owner_app_blueprint)

    from .events_app import events_app as events_app_blueprint
    app.register_blueprint(events_app_blueprint)

    return app
