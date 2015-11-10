from app.mainsite import mainsite

__author__ = 'Frenos'

from datetime import datetime

from flask import render_template
from ..database.models import Currency, BankSlot, Item, PvpMatch, TPTransaction
from ..tasks import updatePrices_async, updateItems_async, updateBank_async, updateTransactions_async, \
    updatePvPMatches_async


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
    chartData = []
    # daten umformatieren fuer Charts
    for archiveItem in archiveData:
        chartData.append([str(archiveItem.time), int(archiveItem.value)])
    # archiveData umdrehen so das neueste Daten oben sind
    archiveData = list(reversed(archiveData))
    return render_template('account_wallet_currency.html', currencyInfo=currencyInfo, archiveData=archiveData,
                           chartData=chartData)


@mainsite.route('/account/bank')
def accountBank():
    bankInfo = BankSlot.query.order_by(BankSlot.id.asc()).all()
    return render_template('account_bank.html', bankInfo=bankInfo)

@mainsite.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@mainsite.route('/pvp/matches')
def pvpMatches():
    matches = PvpMatch.query.order_by(PvpMatch.started.desc()).all()
    return render_template('pvp_matches.html', matches=matches)

@mainsite.route('/items')
@mainsite.route('/items/<int:page>')
def items(page=1):
    pagination = Item.query.paginate(page, 50, False)
    return render_template('items.html', pagination=pagination)


@mainsite.route('/items/details/<int:itemid>')
def itemsDetails(itemid):
    itemObj = Item.query.get(itemid)
    return render_template('items_details.html', item=itemObj)


@mainsite.route('/transactions')
@mainsite.route('/transactions/<int:page>')
def transactions(page=1):
    pagination = TPTransaction.query.order_by(TPTransaction.purchased.desc()).paginate(page, 25, False)
    return render_template('transactions.html', pagination=pagination)

@mainsite.route('/updateAll')
def updateAll():
    updateItems_async.delay()
    updatePrices_async.delay()
    updateBank_async.delay()
    updateTransactions_async.delay()
    updatePvPMatches_async.delay()
    return render_template('index.html',
                           current_time=datetime.utcnow())
