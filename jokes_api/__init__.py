from os import path
from logging.config import dictConfig

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import DefaultConfig, LoggingConfig


__version__ = '0.1.0'


db = SQLAlchemy()
migrate = Migrate()
auth = LoginManager()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)

    if config:
        app.config.from_object(config)

    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise RuntimeError('Database URL is not provided')

    dictConfig(LoggingConfig)

    db.init_app(app)
    auth.init_app(app)

    migrate.init_app(app, db, directory=path.join(app.root_path, 'migrations'))

    from .views import views
    app.register_blueprint(views)

    return app
