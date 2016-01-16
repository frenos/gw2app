from celery.signals import task_postrun

from app import config
from app.database import db
from app.extensions import celery
from app.gw2db.accountDb import AccountDb
from app.gw2db.commonDb import CommonDb
from app.gw2db.itemDb import ItemDb
from factory_celery import create_celery_app

myAccountDb = AccountDb(api_key=config.GW2_API_KEY)
myItemDb = ItemDb(api_key=config.GW2_API_KEY)
myCommonDb = CommonDb(api_key=config.GW2_API_KEY)
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
    for chunk in allIds:
        updateItemsfromList.delay(chunk)


@celery.task(base=celery.Task)
def updateMaps_async():
    celery = create_celery_app()
    myCommonDb.updateMaps()

@celery.task(base=celery.Task)
def updatePvPMatches_async():
    celery = create_celery_app()
    myAccountDb.getPvpMatches()

@celery.task(base=celery.Task)
def updateTransactions_async():
    celery = create_celery_app()
    myAccountDb.getTransactions()

@celery.task(base=celery.Task)
def updateItemsfromList(itemList):
    celery = create_celery_app()
    myItemDb.updateItems(itemList)

@celery.task(base=celery.Task)
def updatePrices_async():
    celery = create_celery_app()
    allIds = myItemDb.getPriceIdChunked()
    for chunk in allIds:
        updatePricesfromList.delay(chunk)
        #jobs = group(updatePricesfromList(chunk) for chunk in allIds).delay()


@celery.task(base=celery.Task)
def updatePricesfromList(itemList):
    celery = create_celery_app()
    myItemDb.updatePrices(itemList)


@celery.task(base=celery.Task)
def updateBank_async():
    celery = create_celery_app()
    myAccountDb.getBankContent()


@celery.task(base=celery.Task)
def updateRecipes_async():
    celery = create_celery_app()
    allIds = myItemDb.getRecipeIdChunked()
    for chunk in allIds:
        updateRecipesfromList.delay(chunk)


@celery.task(base=celery.Task)
def updateRecipesfromList(recipeList):
    celery = create_celery_app()
    myItemDb.getRecipes(itemList=recipeList)

@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.session.remove()
