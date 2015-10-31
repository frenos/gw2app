from celery.signals import task_postrun
from celery import group

from factory_celery import create_celery_app
from app.database import db
from app.gw2db.accountDb import AccountDb
from app.gw2db.itemDb import ItemDb
from app import config
from app.extensions import celery

myAccountDb = AccountDb(api_key=config.GW2_API_KEY)
myItemDb = ItemDb(api_key=config.GW2_API_KEY)
celery = create_celery_app()


@celery.task(base=celery.Task)
def getWalletData_async():
    celery = create_celery_app()
    myAccountDb.updateCurrencies()
    myAccountDb.getWalletData()


@celery.task(base=celery.Task)
def updateItems_async():
    celery = create_celery_app()
    allIds = myItemDb.getItemsChunked()
    jobs = group(updateItemsfromList(chunk) for chunk in allIds)()


@celery.task(base=celery.Task)
def updateItemsfromList(itemList):
    celery = create_celery_app()

    myItemDb.updateItems(itemList)


@celery.task(base=celery.Task)
def updateBank_async():
    celery = create_celery_app()
    myAccountDb.getBankContent()


@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.session.remove()
