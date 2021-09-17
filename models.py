from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class TimestampMixin:
    created_at = db.Column(db.TIMESTAMP, # тип данных,
        default = datetime.utcnow,
        nullable=False
        )
    updated_at = db.Column(db.TIMESTAMP,
        default = datetime.utcnow,      # вычисляется при создании
        onupdate=datetime.utcnow,        # вычисляется каждый раз при обновлении сущности
        nullable=False      # не может быть пустым
        )



class Address(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    small_address = db.Column(db.String(500))
    places = db.relationship('Place', backref='placeaddr')


class Location(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    small_location = db.Column(db.String(500))
    places = db.relationship('Place', backref='placelocat')


class Place(db.Model, TimestampMixin):
    #__table_args__ = (PrimaryKeyConstraint('location_id', 'address_id'),)
    __table_args__ = (UniqueConstraint('location_id', 'address_id', name ='place_address'),)
    id = db.Column(db.Integer, primary_key=True)
    id_gmc = db.Column(db.String(10), default='no', comment='ID_GMC')
    devices = db.relationship('Device', backref = 'place', uselist = False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'))




class Device(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_aiu = db.Column(db.String(10), comment='ID_AIU', nullable=False, unique=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))



class Switch(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    ports = db.relationship('Port', backref='swports')

class Port(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    places = db.relationship('Place', backref='placeport')
