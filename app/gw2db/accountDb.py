from datetime import datetime

__author__ = 'Frenos'
from ..gw2api.apiclient import ApiClient
from ..database import db
from ..database.models import WalletData, Currency, BankSlot, Item


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

    def getBankContent(self):
        bankContents = self.apiClient.getBankContent()
        # list(enumerate(list)) erzeugt neue list mit [(index, value), ..]
        for bankSlot in list(enumerate(bankContents)):
            slotId = bankSlot[0]
            if bankSlot[1]:
                item = Item.query.get(bankSlot[1]['id'])
                if not item:
                    itemResponse = self.apiClient.getItem(itemId=bankSlot[1]['id'])
                    for item in itemResponse:
                        itemId = item['id']
                        # prep values and errorcheck
                        if 'name' in item:
                            newName = item['name']
                        else:
                            newName = None
                        if 'icon' in item:
                            newIcon = item['icon']
                        else:
                            newIcon = None
                        if 'description' in item:
                            newDescription = item['description']
                        else:
                            newDescription = None
                        if 'level' in item:
                            newLevel = item['level']
                        else:
                            newLevel = 99
                        if 'vendor_value' in item:
                            newVendVal = item['vendor_value']
                        else:
                            newVendVal = 0

                        item = Item(
                            id=itemId,
                            name=newName,
                            icon=newIcon,
                            description=newDescription,
                            type=None,
                            rarity=None,
                            level=newLevel,
                            vendor_value=newVendVal,
                        )
                        db.session.add(item)
                        db.session.commit()

                count = bankSlot[1]['count']
            else:
                item = None
                count = 0
            bankSlotObject = BankSlot.query.get(bankSlot[0])
            if bankSlotObject:
                bankSlotObject.id = slotId
                bankSlotObject.count = count
                bankSlotObject.item = item
            else:
                newBankSlot = BankSlot(id=slotId, item=item, count=count)
                db.session.add(newBankSlot)
                db.session.commit()
