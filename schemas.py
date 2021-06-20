
from database import Base
from pydantic import BaseModel
from typing import List,Optional


class Projet(BaseModel):
    type_panel:str
    pmax:int
    imx:int
    dimension:int
    description:str 
    name_projet:str
    nb_panel:int
    temp:int
    localisation:str
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


class Sensor(BaseModel):
    sensor_name:str
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
    type_panel:str
    pmax:int
    imx:int
    dimension:int
    description:str 
    name_projet:str
    nb_panel:int
    temp:int
    localisation:str
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
        
        
class Showsensor(BaseModel):
    sensor_name:str
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
    



        
        

