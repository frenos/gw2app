from app.mainsite import mainsite

__author__ = 'Frenos'

from datetime import datetime

from flask import render_template
from ..database.models import Currency
from ..tasks import getWalletData_async


@mainsite.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())


@mainsite.route('/account/wallet')
def accountWallet():
    walletData = []
    currencies = Currency.query.order_by(Currency.order.asc()).all()
    for currency in currencies:
        if currency.archiveData:
            value = currency.archiveData[-1].value
        else:
            value = 0
        walletData.append({"id": currency.id,
                           "icon": currency.icon,
                           "name": currency.name,
                           "description": currency.description,
                           "value": value})

    return render_template('account_wallet.html', walletData=walletData)


@mainsite.route('/account/wallet/<int:currencyID>')
def accountWalletDetail(currencyID):
    currencyInfo = Currency.query.get(currencyID)
    if not currencyInfo:
        return index()
    archiveData = currencyInfo.archiveData
    return render_template('account_wallet_currency.html', currencyInfo=currencyInfo, archiveData=archiveData)


@mainsite.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@mainsite.route('/testupdate')
def testUpdate():
    getWalletData_async.delay()

    # tasks.updateWalletData_async.delay()
    return render_template('index.html', current_time=datetime.utcnow())
