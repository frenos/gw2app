from flask import Flask, Blueprint
import chartkick

from app.database import db
from app.extensions import celery
from app.extensions import moment
from app.extensions import bootstrap
from app.extensions import config
import app.utils as utils
from app.gw2db import gw2db
from app.gw2api import gw2api
from app.mainsite import mainsite


def create_app():
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
    myChartkick = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
    app.register_blueprint(myChartkick, url_prefix='/ck')

def register_jinja_env(app):
    app.jinja_env.globals['url_for_other_page'] = utils.url_for_other_page
    app.jinja_env.globals['timeago'] = utils.timeago
    app.jinja_env.add_extension('chartkick.ext.charts')
