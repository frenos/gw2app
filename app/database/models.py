__author__ = 'Frenos'
from app.database import db


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text())
    icon = db.Column(db.Text())
    description = db.Column(db.Text())
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    rarity_id = db.Column(db.Integer, db.ForeignKey('rarities.id'))
    level = db.Column(db.Integer)
    vendor_value = db.Column(db.Integer)
    flags = db.relationship('ItemFlag', backref='item')
    game_types = db.relationship('ItemGameType', backref='item')
    restrictions = db.relationship('ItemRestriction', backref='item')
    # TODO:cross-reference Skin-ID to Skin-Api?
    default_skin = db.Column(db.Integer)
    bankslots = db.relationship('BankSlot', backref='item')
    recipe = db.relationship('Recipe', backref='output_item')
    recipeIngredient = db.relationship('RecipeIngredient', backref='item')
    priceData = db.relationship('PriceData')
    transactions = db.relationship('TPTransaction', backref='item')


class ItemFlag(db.Model):
    __tablename__ = 'itemflags'
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    flag = db.Column(db.Text())


class ItemGameType(db.Model):
    __tablename__ = 'itemgametypes'
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    game_type = db.Column(db.Text())


class ItemRestriction(db.Model):
    __tablename__ = 'itemrestrictions'
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    restriction = db.Column(db.Text())

class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    items = db.relationship('Item', backref='type')


class Rarity(db.Model):
    __tablename__ = 'rarities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    items = db.relationship('Item', backref='rarity')


class TPTransaction(db.Model):
    __tablename__ = 'TPtransactions'
    id = db.Column(db.BigInteger, primary_key=True)
    created = db.Column(db.DateTime)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    type = db.Column(db.Text)
    price = db.Column(db.Integer)
    purchased = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)


class TPTransaction_broken(db.Model):
    __tablename__ = 'TPtransactions_broken'
    id = db.Column(db.BigInteger, primary_key=True)
    created = db.Column(db.DateTime)
    item_id = db.Column(db.Integer)
    type = db.Column(db.Text)
    price = db.Column(db.Integer)
    purchased = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)

class Currency(db.Model):
    __tablename__ = 'currencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    icon = db.Column(db.Text())
    order = db.Column(db.Integer)
    archiveData = db.relationship('WalletData', backref='currency')

class PriceData(db.Model):
    __tablename__ = 'pricedata'
    id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    buyQuantity = db.Column(db.Integer)
    buyPrice = db.Column(db.Integer)
    sellQuantity = db.Column(db.Integer)
    sellPrice = db.Column(db.Integer)

class WalletData(db.Model):
    __tablename__ = 'walletdata'
    dataId = db.Column(db.Integer, primary_key=True)
    currencyId = db.Column(db.Integer, db.ForeignKey('currencies.id'))
    value = db.Column(db.Integer)
    time = db.Column(db.DateTime)

class BankSlot(db.Model):
    __tablename__ = 'bankslots'
    id = db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer, db.ForeignKey('items.id'))
    count = db.Column(db.Integer)


class PvpMatch(db.Model):
    __tablename__ = 'pvpmatches'
    id = db.Column(db.String(50), primary_key=True)
    map_id = db.Column(db.Integer, db.ForeignKey('maps.id'))
    started = db.Column(db.DateTime)
    ended = db.Column(db.DateTime)
    result = db.Column(db.Text)
    team = db.Column(db.Text)
    profession = db.Column(db.Text)
    score_red = db.Column(db.Integer)
    score_blue = db.Column(db.Integer)


class Map(db.Model):
    __tablename__ = 'maps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    min_level = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    region_id = db.Column(db.Integer)
    region_name = db.Column(db.Text)
    continent_id = db.Column(db.Integer)
    continent_name = db.Column(db.Text)
    matches = db.relationship('PvpMatch', backref='map')


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text())
    output_item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    output_item_count = db.Column(db.Integer)
    disciplines = db.relationship('RecipeDiscipline', backref='recipe')
    min_rating = db.Column(db.Integer)
    ingredients = db.relationship('RecipeIngredient', backref='recipe')
    chat_link = db.Column(db.Text())


class RecipeDiscipline(db.Model):
    __tablename__ = 'recipedisciplines'
    id = db.Column(db.Integer, primary_key=True)
    recipeId = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    discipline = db.Column(db.Text())


class RecipeIngredient(db.Model):
    __tablename__ = 'recipeingredients'
    id = db.Column(db.Integer, primary_key=True)
    recipeId = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    count = db.Column(db.Integer)
