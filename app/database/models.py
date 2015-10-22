__author__ = 'Frenos'
from app.database import db


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64))
    icon = db.Column(db.String(128))
    description = db.Column(db.String(128))
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    rarity_id = db.Column(db.Integer, db.ForeignKey('rarities.id'))
    level = db.Column(db.Integer)
    vendor_value = db.Column(db.Integer)

    # TODO:cross-reference Skin-ID to Skin-Api?
    default_skin = db.Column(db.Integer)


class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    items = db.relationship('Item', backref='type')


class Rarity(db.Model):
    __tablename__ = 'rarities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    items = db.relationship('Item', backref='rarity')


class Currency(db.Model):
    __tablename__ = 'currencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    icon = db.Column(db.String(128))
    order = db.Column(db.Integer)
    archiveData = db.relationship('WalletData', backref='currency')


class WalletData(db.Model):
    __tablename__ = 'walletdata'
    dataId = db.Column(db.Integer, primary_key=True)
    currencyId = db.Column(db.Integer, db.ForeignKey('currencies.id'))
    value = db.Column(db.Integer)
    time = db.Column(db.DateTime)
