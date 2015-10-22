from flask import Flask

from app.database import db
from app.extensions import celery
from app.extensions import moment
from app.extensions import bootstrap
import app.utils as utils
from app.gw2db import gw2db
from app.gw2api import gw2api
from app.mainsite import mainsite


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_jinja_env(app)

    return app


def register_extensions(app):
    db.init_app(app)
    celery.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(gw2db)
    app.register_blueprint(gw2api)
    app.register_blueprint(mainsite)


def register_jinja_env(app):
    app.jinja_env.globals['url_for_other_page'] = utils.url_for_other_page
    app.jinja_env.globals['timeago'] = utils.timeago
