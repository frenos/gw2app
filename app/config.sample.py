import os

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class base_config(object):
    SITE_NAME = 'gw2app'
    SERVER_NAME = os.environ.get('SERVER_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CELERY_BROKER_URL = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_BACKEND = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379/0')
    CELERY_IMPORTS = ('app.tasks',)
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    GW2_API_KEY = ""

    CELERYBEAT_SCHEDULE = {
        'WalletData-every-hour': {
            'task': 'app.tasks.getWalletData_async',
            'schedule': crontab(minute=0, hour='*')
        },
        'updateItemDb-every-4-hours': {
            'task': 'app.tasks.updateItems_async',
            'schedule': crontab(minute=10, hour='*/4')
        }
    }

    SQLALCHEMY_DATABASE_URI = 'mysql://gw2app:gw2app@localhost/gw2app'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class dev_config(base_config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class test_config(base_config):
    TESTING = True
