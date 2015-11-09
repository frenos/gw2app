from datetime import datetime, timedelta

__author__ = 'Frenos'
from ..gw2api.apiclient import ApiClient
from ..database import db
from ..database.models import WalletData, Currency, BankSlot, Item, TPTransaction, TPTransaction_broken, PvpMatch
import dateutil.parser


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


    def getPvpMatches(self):
        matches = self.apiClient.getPvPMatchDetails()
        for match in matches:
            matchObj = PvpMatch.query.get(match['id'])
            if not matchObj:
                id = match['id']
                map_id = match['map_id']
                started = dateutil.parser.parse(match['started'])
                ended = dateutil.parser.parse(match['ended'])
                # fix timestamps because api returns utc+8
                started = started - timedelta(hours=8)
                ended = ended - timedelta(hours=8)
                result = match['result']
                team = match['team']
                profession = match['profession']
                score_red = match['scores']['red']
                score_blue = match['scores']['blue']
                newMatch = PvpMatch(id=id,
                                    map_id=map_id,
                                    started=started,
                                    ended=ended,
                                    result=result,
                                    team=team,
                                    profession=profession,
                                    score_red=score_red,
                                    score_blue=score_blue
                                    )
                db.session.add(newMatch)
        db.session.commit()


    def getTransactions(self):
        transactions = self.apiClient.getTransactionsHistory(sells=True)
        self.writeTransactions(transactions, sells=True)
        transactions = self.apiClient.getTransactionsHistory(buys=True)
        self.writeTransactions(transactions, buys=True)

    def writeTransactions(self, transactions, sells=None, buys=None):
        if sells:
            type = 'sell'
        elif buys:
            type = 'buy'
        else:
            type = 'error'
        for transaction in transactions:
            transactionObj = TPTransaction.query.get(long(transaction['id']))
            if not transactionObj:
                id = transaction['id']
                created = dateutil.parser.parse(transaction['created'])
                item_id = int(transaction['item_id'])
                price = transaction['price']
                purchased = dateutil.parser.parse(transaction['purchased'])
                quantity = transaction['quantity']
                itemObj = Item.query.get(item_id)
                if itemObj:
                    newTransaction = TPTransaction(id=id,
                                                   created=created,
                                                   item_id=item_id,
                                                   type=type,
                                                   price=price,
                                                   purchased=purchased,
                                                   quantity=quantity)
                    db.session.add(newTransaction)
                else:
                    if not TPTransaction_broken.query.get(id):
                        newTransaction = TPTransaction_broken(id=id,
                                                              created=created,
                                                              item_id=item_id,
                                                              type=type,
                                                              price=price,
                                                              purchased=purchased,
                                                              quantity=quantity)
                        db.session.add(newTransaction)
        db.session.commit()
