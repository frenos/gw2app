from flask.ext.celery import Celery

celery = Celery()

from flask.ext.moment import Moment

moment = Moment()

from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

from config import dev_config

config = dev_config
