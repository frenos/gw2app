from flask import Flask
from celery import Celery

from app.database import db
from app.extensions import celery, bootstrap, moment, config
import app.utils as utils
from app.gw2db import gw2db
from app.gw2api import gw2api


def create_app(_config=config):
    app = Flask(__name__)
    app.config.from_object(_config)

    register_extensions(app)
    register_blueprints(app)
    register_jinja_env(app)

    return app


def create_celery_app(app=None):
    app = app or create_app(config)
    app.config.from_object(config)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def register_extensions(app):
    db.init_app(app)
    celery.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(gw2db)
    app.register_blueprint(gw2api)


def register_jinja_env(app):
    app.jinja_env.globals['url_for_other_page'] = utils.url_for_other_page
    app.jinja_env.globals['timeago'] = utils.timeago
