
from database import Base
from pydantic import BaseModel
from typing import List,Optional


class Projet(BaseModel):
    typepv:str
    vmx:str
    imx:str
    pmx:str
    temp:str
    long:str
    lat:str
    class Config:
        orm_mode = True


class Gatewaye(BaseModel):
    name:str
    class Config:
        orm_mode = True
        

class Device(BaseModel):
    name:str
    class Config:
        orm_mode = True


class User(BaseModel):
    name:str
    email:str
    password:str
  
    
class Showuser(BaseModel):
    name:str
    email:str
    projets:List[Projet] = []
    class Config:
        orm_mode = True



class Showprojet(BaseModel):
    typepv:str
    vmx:str
    imx:str
    pmx:str 
    temp:str
    long:str
    lat:str
    creator:Showuser
    gatewayes:List[Gatewaye] = []
    class Config:
        orm_mode = True
        
        
class Showgw(BaseModel):
    name:str
    devices:List[Device] = []
    class Config:
        orm_mode = True
        
        
class Showdevice(BaseModel):
    name:str
    class Config:
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str
    
    
    
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    



        
        

