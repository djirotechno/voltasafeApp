
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Projet(Base):
    __tablename__ = 'projets'
    id = Column(Integer,primary_key=True,index=True)
    name_projet = Column(String)
    description = Column(String)
    nb_panel = Column(Integer)
    type_panel = Column(String)
    pmax = Column(Integer)
    imx = Column(Integer)
    dimension = Column(Integer)
    temp = Column(Integer)
    localisation = Column(String)
    user_id = Column(Integer,ForeignKey('users.id'))
    
    creator = relationship("User", back_populates="projets")
    gatewayes = relationship('Gatewaye', back_populates="gw_owne")

  

    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    projets= relationship('Projet', back_populates="creator")
    

class Gatewaye(Base):
    __tablename__ = 'gatewayes'
    
    id = Column(Integer,primary_key=True,index=True)
    g_id = Column(String)
    name = Column(String)
    projet_id = Column(Integer,ForeignKey('projets.id'))
    gw_owne = relationship("Projet", back_populates="gatewayes")
    devices = relationship("Device", back_populates="device_owne")

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer,primary_key=True,index=True)
    d_id = Column(String)
    name = Column(String)
    gw_id = Column(Integer,ForeignKey('gatewayes.id'))
    device_owne = relationship("Gatewaye", back_populates="devices")
    sensors = relationship("Sensor",back_populates="sensor_owne")
    
    
    
class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer,primary_key=True,index=True)
    s_id = Column(String)
    sensor_name = Column(String)
    unit = Column(String)
    type_sensor = Column(String)
    sensor_owne = relationship("Device", back_populates="sensors")
    device_id = Column(Integer,ForeignKey('devices.id'))
    
   