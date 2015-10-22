from datetime import datetime

__author__ = 'Frenos'
from ..gw2api.apiclient import ApiClient
from ..database import db
from ..database.models import WalletData, Currency


class AccountDb:
    def __init__(self, api_key):
        self.apiClient = ApiClient(api_key)

    def updateCurrencies(self):
        currencies = self.apiClient.getCurrencies()
        for currency in currencies:

            if 'name' in currency:
                newName = currency['name']
            else:
                newName = None
            if 'id' in currency:
                newId = currency['id']
            else:
                newId = None
            if 'order' in currency:
                newOrder = currency['order']
            else:
                newOrder = None
            if 'description' in currency:
                newDescription = currency['description']
            else:
                newDescription = None
            if 'icon' in currency:
                newIcon = currency['icon']
            else:
                newIcon = None

            currencyObject = Currency.query.get(currency['id'])
            if currencyObject:
                currencyObject.name = newName
                currencyObject.description = newDescription
                currencyObject.icon = newIcon
                currencyObject.order = newOrder
                db.session.add(currencyObject)
            else:
                newCurrency = Currency(id=newId, name=newName, description=newDescription, icon=newIcon, order=newOrder)
                db.session.add(newCurrency)

        db.session.commit()

    def getWalletData(self):
        walletData = self.apiClient.getWalletContent()
        for data in walletData:
            currencyObject = Currency.query.get(data['id'])
            newData = WalletData(currency=currencyObject, value=data['value'], time=datetime.utcnow())
            db.session.add(newData)
        db.session.commit()
