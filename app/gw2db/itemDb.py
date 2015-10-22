__author__ = 'Frenos'

from ..gw2api.apiclient import ApiClient
from ..database import db
from ..database.models import Item, Rarity, Type


class ItemDb:
    def __init__(self, api_key):
        self.apiClient = ApiClient(api_key)

    def updateItems(self):
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
            if 'level' in item:
                newLevel = item['level']
            else:
                newLevel = 99
            if 'vendor_value' in item:
                newVendVal = item['vendor_value']
            else:
                newVendVal = 0

            itemObject = Item.query.filter_by(id=itemId).first()
            if itemObject:

                itemObject.name = newName
                itemObject.icon = newIcon
                itemObject.description = newDescription
                itemObject.type = self.getTypeObj(item['type'])
                itemObject.rarity = self.getRarityObj(item['rarity'])
                itemObject.level = newLevel
                itemObject.vendor_value = newVendVal
                db.session.add(itemObject)

            else:
                newItem = Item(
                    id=itemId,
                    name=newName,
                    icon=newIcon,
                    description=newDescription,
                    type=self.getTypeObj(item['type']),
                    rarity=self.getRarityObj(item['rarity']),
                    level=newLevel,
                    vendor_value=newVendVal,
                )
                db.session.add(newItem)
            db.session.commit()

    def getTypeObj(self, myType):
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
