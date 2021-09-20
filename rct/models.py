#from flask_login import UserMixin

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

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
    small_address = db.Column(db.String(50), comment='small_address')
    rgis_address  = db.Column(db.String(200), comment='rgis')
    district = db.Column(db.String(50), default='Красносельский', comment='rayon')
    places = db.relationship('Place', backref='placeaddr')
    vlans = db.relationship('Vlan', backref='addressvlans')


class Location(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    small_location = db.Column(db.String(500))
    places = db.relationship('Place', backref='placelocat')


class Place(db.Model, TimestampMixin):
    #__table_args__ = (PrimaryKeyConstraint('location_id', 'address_id'),)
    __table_args__ = (UniqueConstraint('location_id', 'address_id', name ='place_address'),)
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(50), default='no', comment='name')
    id_gmc = db.Column(db.String(10), default='no', comment='ID_GMC')
    description_gmc = db.Column(db.String(10), default='no', comment='description-GMC')
    lng = db.Column(db.Integer, default='0', comment='long')
    lat = db.Column(db.Integer, default='0', comment='lat')
    rtsp = db.Column(db.String(40), default='no', comment='rtsp')
    cam_type = db.Column(db.String(40), default='no', comment='type')
    devices = db.relationship('Device', backref = 'place', uselist = False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'))
    azimuth = db.Column(db.String(15), default='no', comment='azimut')
    angle = db.Column(db.String(15), default='no', comment='angel')
    n_gk = db.Column(db.String(15), default='GK-', comment='N_GK')
    osd_menu = db.Column(db.String(15), default='OSD', comment='osd')
    screen_pth_v1 = db.Column(db.String(100), default='no', comment='screen_first')
    screen_pth_v2 = db.Column(db.String(100), default='no', comment='screen_last')
    vlan_id = db.Column(db.Integer, db.ForeignKey('vlan.id'), nullable=False)
    active = db.Column(db.Boolean, default = True, nullable = False, comment = 'ONLINE или OFFLINE')

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), default='vds-', comment='name_server')
    ipaddr_id = db.Column(db.Integer, db.ForeignKey('ipaddr.id'))
    devices = db.relationship('Device', backref='deviceserver')


class Ipaddr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.String(26), default='0.0.0.0', comment='ipaddr')
    devices = db.relationship('Device', backref='deviceip', uselist = False)
    servers = db.relationship('Server', backref='serverip', uselist = False)


class Vlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_vl = db.Column(db.Integer, nullable=False, comment='id_vlan')
    name = db.Column(db.String(14), nullable=False, comment='name_vlan')
    placeses = db.relationship('Place', backref = 'vlanplace')
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

class Device(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_aiu = db.Column(db.String(10), comment='ID_AIU', nullable=False, unique=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    cam_type = db.Column(db.String(40), default='no', comment='type')
    vendor = db.Column(db.String(40), default='hikvision', comment='vendor')
    model = db.Column(db.String(40), default='no', comment='vendor')
    ipaddr_id = db.Column(db.Integer, db.ForeignKey('ipaddr.id'),  unique=True)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))


class Switch(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    ports = db.relationship('Port', backref='swports')
    type = db.Column(db.String(10), default = 'sw', comment = 'sw-swu-core')



class Port(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    Switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'))
    places = db.relationship('Place', backref='placeport')
    status = db.Column(db.String(10), default = 'off', comment = 'empty')
    link = db.Column(db.String(10), default = 'access', comment = 'uplink-downlink')


