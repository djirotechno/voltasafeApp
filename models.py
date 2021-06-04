from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Projet(Base):
    __tablename__ = 'projets'
    
    id = Column(Integer,primary_key=True,index=True)
    typepv = Column(String)
    vmx = Column(String)
    imx = Column(String)
    pmx = Column(String)
    temp = Column(String)
    long = Column(String)
    lat = Column(String)
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
    name = Column(String)
    projet_id = Column(Integer,ForeignKey('projets.id'))
    gw_owne = relationship("Projet", back_populates="gatewayes")
    device_owne = relationship("Device", back_populates="gatewayes")

class Device(Base):
    __tablename__ = 'devices'
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    gw_id = Column(Integer,ForeignKey('gatewayes.id'))
    device_owne = relationship("Gatewaye", back_populates="devices")