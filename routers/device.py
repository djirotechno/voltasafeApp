
from fastapi import APIRouter

from typing import Optional,List
from fastapi_login import LoginManager
from fastapi import FastAPI, Request,Depends,status,Form
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.utils.decor import deprecated_function
from pydantic.typing import new_type_supertype
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import user
from starlette.responses import Response
from starlette.status import HTTP_302_FOUND
import schemas,models
from database import SessionLocal, engine,get_db
from sqlalchemy.orm import Session, session 
import token_0
from hashing import Hash
import oauth2
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import RedirectResponse,HTMLResponse




templates = Jinja2Templates(directory="templates")

router = APIRouter()

# #######################################################################
#
#                              CRUD DEVICES       include_in_schema=False                      
#
#########################################################################

@router.post("/device",tags=["Device"])
def create_device(db:Session=Depends(get_db),
           deviceName:str = Form(...),
           gw_id:int= Form(...),
           d_id:str = Form(...)):
      newdevice = models.Device(
            name = deviceName,
            gw_id = gw_id,
            d_id = d_id)
      db.add(newdevice)
      db.commit()       
      return RedirectResponse(url="/devices", status_code=HTTP_302_FOUND)
      

@router.get('/device',response_model=List[schemas.Showdevice], tags=["Device"] )
def get_devices(request:Request,db:Session = Depends(get_db) ):
       devices = db.query(models.Device).all()
       return templates.TemplateResponse("devices/show_device.html", {"request": request, "devices":devices})
       
      
@router.get('/devices',response_model=List[schemas.Showdevice],include_in_schema=False )
def all(request:Request,db:Session = Depends(get_db) ):
       devices = db.query(models.Device).all()
      #  return templates.TemplateResponse("devices/show_device.html", {"request": request, "devices":devices})
       return devices
      
      
      
@router.get('/device/{device_id}',response_model=schemas.Showdevice,tags=["Device"])
def show(id,request:Request ,db:Session = Depends(get_db)):
      deviceshow = db.query(models.Device).filter(models.Device.id == id).first()
     
      # if not device:
      #       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      return templates.TemplateResponse("devices/show_device.html", {"request": request, "deviceshow": deviceshow  })
      

@router.put('/device/{device_id}/name',status_code=status.HTTP_202_ACCEPTED,tags=["Device"])
def update(id,request: schemas.Device,db:Session = Depends(get_db)):
     projet = db.query(models.Device).filter(models.Device.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@router.delete('/device/{device_id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Device"])
def destroy(id,db:Session = Depends(get_db)):
      db.query(models.Device).filter(models.Device.id == id).delete()
      db.commit()
      return 'done'


@router.put('/device/{device_id}/gatewaye_id',status_code=status.HTTP_202_ACCEPTED,tags=["Device"])
def update_gatewaye(id,request: schemas.Device,db:Session = Depends(get_db)):
     Device = db.query(models.Device).filter(models.Device.id == id)
     if not Device.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     Device.update(request)
     db.commit()
     return "update"

