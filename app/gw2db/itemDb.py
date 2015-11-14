__author__ = 'Frenos'

from ..gw2api.apiclient import ApiClient
from ..database import db
from ..database.models import Item, Rarity, Type, PriceData, ItemFlag, ItemGameType, ItemRestriction


class ItemDb:
    """
    Class to create relationship between Database and Api for everything concerning items.
    """
    def __init__(self, api_key):
        self.apiClient = ApiClient(api_key)

    def getPriceIdChunked(self):
        return self.apiClient.getPriceIdsChunked()

    def updatePrices(self, itemList=None):
        """
        Will update the prices and buy/sell quantities either from a given list of items or all available items
        @param itemList: list of ids to update
        @return: no return value
        """
        if itemList:
            allItemPrices = self.apiClient.getPrice(idsString=itemList)
        else:
            allItemPrices = self.apiClient.getAllPrices()

        for priceInfo in allItemPrices:
            itemId = priceInfo['id']
            # check if we know the item before:
            itemObj = Item.query.get(int(itemId))
            if not itemObj:
                continue
            buyQuantity = priceInfo['buys']['quantity']
            buyPrice = priceInfo['buys']['unit_price']
            sellQuantity = priceInfo['sells']['quantity']
            sellPrice = priceInfo['sells']['unit_price']

            priceDataObj = PriceData.query.get(itemId)
            if priceDataObj:
                priceDataObj.id = itemId
                priceDataObj.buyQuantity = buyQuantity
                priceDataObj.buyPrice = buyPrice
                priceDataObj.sellQuantity = sellQuantity
                priceDataObj.sellPrice = sellPrice
                db.session.add(priceDataObj)
            else:
                newPriceData = PriceData(
                    id=itemId,
                    buyQuantity=buyQuantity,
                    buyPrice=buyPrice,
                    sellQuantity=sellQuantity,
                    sellPrice=sellPrice
                )
                db.session.add(newPriceData)
        db.session.commit()

    def getItemsChunked(self):
        return self.apiClient.getItemIdsChunked()

    def updateItems(self, itemList=None):
        """
        Will update the information either about items given in itemList or all available items.
        @param itemList: list of ids to update
        @return: no return value
        """
        if itemList:
            allItemInformation = self.apiClient.getItem(idsString=itemList)
        else:
            allItemInformation = self.apiClient.getAllItems()

        for item in allItemInformation:
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
            if 'flags' in item and len(item['flags']) > 0:
                flags = item['flags']
            else:
                flags = None
            if 'game_types' in item and len(item['game_types']) > 0:
                game_types = item['game_types']
            else:
                game_types = None
            if 'restrictions' in item and len(item['restrictions']) > 0:
                restrictions = item['restrictions']
            else:
                restrictions = None

            if 'level' in item:
                newLevel = item['level']
            else:
                newLevel = 99
            if 'vendor_value' in item:
                newVendVal = item['vendor_value']
            else:
                newVendVal = 0

            itemObject = Item.query.get(itemId)
            if itemObject:

                itemObject.name = newName
                itemObject.icon = newIcon
                itemObject.description = newDescription
                itemObject.type = self.getTypeObj(item['type'])
                itemObject.rarity = self.getRarityObj(item['rarity'])
                itemObject.level = newLevel
                itemObject.vendor_value = newVendVal
                if flags:
                    for flag in flags:
                        flagObj = ItemFlag.query.filter_by(itemId=itemId).filter_by(flag=flag).first()
                        if not flagObj:
                            newFlag = ItemFlag(itemId=itemId, flag=flag)
                            itemObject.flags.append(newFlag)
                if game_types:
                    for game_type in game_types:
                        game_typeObj = ItemGameType.query.filter_by(itemId=itemId).filter_by(
                            game_type=game_type).first()
                        if not game_typeObj:
                            newGameType = ItemGameType(itemId=itemId, game_type=game_type)
                            itemObject.game_types.append(newGameType)
                if restrictions:
                    for restriction in restrictions:
                        restrictionObj = ItemRestriction.query.filter_by(itemId=itemId).filter_by(
                            restriction=restriction).first()
                        if not restrictionObj:
                            newRestriction = ItemRestriction(itemId=itemId, restriction=restriction)
                            itemObject.restrictions.append(newRestriction)
                db.session.add(itemObject)

            else:
                newFlags = []
                if flags:
                    for flag in flags:
                        newFlag = ItemFlag(itemId=itemId, flag=flag)
                        newFlags.append(newFlag)
                newGameTypes = []
                if game_types:
                    for game_type in game_types:
                        newGameType = ItemGameType(itemId=itemId, game_type=game_type)
                        newGameTypes.append(newGameType)
                newRestrictions = []
                if restrictions:
                    for restriction in restrictions:
                        newRestriction = ItemRestriction(itemId=itemId, restriction=restriction)
                        newRestrictions.append(newRestriction)
                newItem = Item(
                    id=itemId,
                    name=newName,
                    icon=newIcon,
                    description=newDescription,
                    type=self.getTypeObj(item['type']),
                    rarity=self.getRarityObj(item['rarity']),
                    level=newLevel,
                    vendor_value=newVendVal,
                    flags=newFlags,
                    game_types=newGameTypes,
                    restrictions=newRestrictions
                )
                db.session.add(newItem)
        db.session.commit()

    def getTypeObj(self, myType):
        """
        Will return the Type_Object from Database or create a new item and return it.
        @param myType: String-value of Obj to return
        @return: TypeObj
        """
        typeObject = Type.query.filter_by(name=myType).first()

        # wir kennen den typ schon
        if typeObject:
            return typeObject
        # neuer Typ
        else:
            newType = Type(name=myType)
            db.session.add(newType)
            db.session.commit()
            return newType

    def getRarityObj(self, myRarity):
        """
        Will return the Rarity_Object from Database or create a new Rarity and return it.
        @param myRarity: String-value of Obj to return
        @return: RarityObj
        """
        rarityObject = Rarity.query.filter_by(name=myRarity).first()

        # wir kennen die rarity schon
        if rarityObject:
            return rarityObject
        # neue rarity
        else:
            newRarity = Rarity(name=myRarity)
            db.session.add(newRarity)
            db.session.commit()
            return newRarity
