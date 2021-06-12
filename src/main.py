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
from database import SessionLocal, engine
from sqlalchemy.orm import Session, session 
import token_0
from hashing import Hash
import oauth2
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import RedirectResponse,HTMLResponse
# a0pqy1y5_ARyUZxS9h6ZBxsvckdViExBe69FBDRy1      a0pqy1y5
  # ,get_current_user:schemas.User = Depends(oauth2.get_current_user)
  
SECRET= "a0pqy1y5_ARyUZxS9h6ZBxsvckdViExBe69FBDRy1"
manager = LoginManager(SECRET,token_url="/auth/login")

models.Base.metadata.create_all(engine)

app = FastAPI( 
    title="VoltaSafe API",
    description="Description...",
    version="0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():

      db = SessionLocal()
      try:
            yield db
      finally:
            db.close()
            
@app.get('/home',tags=["Home"])
def home(request:Request):
      return templates.TemplateResponse('home.html',{"request":request})            
# #######################################################################
#
#  Route Formulaire Crèe Projets , Gatewayes, Devices, Sensors
#
#########################################################################
@app.get('/form_projet',tags=["Add"])
def get_form(request:Request):
      return templates.TemplateResponse('/projets/add_projet.html',{"request":request})        

@app.get('/form_gw',tags=["Add"],response_model=List[schemas.Showprojet])
def get_form(request:Request,db:Session=Depends(get_db)):
      projets = db.query(models.Projet).all()
      return templates.TemplateResponse('/gatewayes/add_gw.html',{"request":request,"projets":projets})  
    
@app.get('/form_device',tags=["Device"],response_model=List[schemas.Showdevice])
def get_form(request:Request,db:Session=Depends(get_db)):
     
      gatewayes = db.query(models.Gatewaye).all()
   
      return templates.TemplateResponse("devices/add_device.html", {"request": request,
                                                                    "gatewaye": gatewayes,
                                                                    
                                                                    })


@app.get('/form_sensor',tags=["Add"])
def get_form(request:Request,db:Session=Depends(get_db)):
       devices = db.query(models.Device).all()
       return templates.TemplateResponse('/sensors/add_sensor.html',{"request":request,"devices":devices})  


# #######################################################################
#
#                           CRUD PROJETS
#
#########################################################################

            
@app.post("/projet/",tags=["Projets"])
def project(db:Session=Depends(get_db),
            name_projet:str = Form(...),
            description:str = Form(...),
            nb_panel:int = Form(...),
            type_panel:str = Form(...),
            dimension:int = Form(...),
            pmax:int = Form(...),
            imx:int = Form(...),
            temp:int = Form(...),
            localisation:str = Form(...),
            user_id = 1        
            ):
      new_projet = models.Projet(
            name_projet= name_projet,
            description=description,
            nb_panel=nb_panel,
            type_panel=type_panel,
            dimension=dimension,
            pmax=pmax,
            imx=imx,
            temp=temp,
            localisation = localisation,
            user_id = user_id)
      db.add(new_projet)
      db.commit()
      db.refresh(new_projet)
      
      return RedirectResponse(url="/projets", status_code=HTTP_302_FOUND)
            
            
@app.get('/projets',response_model=List[schemas.Showprojet],  tags=["Projets"])
def all(request:Request,db:Session = Depends(get_db) ):
       projets = db.query(models.Projet).all()
       return templates.TemplateResponse("projets/show_projet.html", {"request": request, "projets": projets})


@app.get('/projet/{id}',status_code=200,response_model=schemas.Showprojet,tags=["Projets"])
def show(id,request:Request ,db:Session = Depends(get_db)):
      projet = db.query(models.Projet).filter(models.Projet.id == id).first()
      if not projet:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      # return templates.TemplateResponse("projet.html", {"request": request, "projets": projet  })
      return projet 

@app.put('/projet/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["Projets"])
def update(id,request: schemas.Projet,db:Session = Depends(get_db)):
     projet = db.query(models.Projet).filter(models.Projet.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.delete('/projet/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Projets"])
def destroy(id,db:Session = Depends(get_db)):
      db.query(models.Projet).filter(models.Projet.id == id).delete()
      db.commit()
      return 'done'


# #######################################################################
#
#                              CRUD USERS
#
#########################################################################

@app.post('/user',tags=["Users"])
def create_user(request:schemas.User,db:Session=Depends(get_db)):
      hashedPassword = Hash.bcrypt(request.password)
      new_user = models.User(name = request.name,email = request.email,password = hashedPassword)
      # new_user = models.User(name = request.name,email = request.email,password = request.password)
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
      
      return 'done'
            
@app.get('/users',response_model=List[schemas.Showuser],tags=["Users"])
def all_user(db:session = Depends(get_db)):
      allusers = db.query(models.User).all()
      return allusers

@app.get('/',response_class=HTMLResponse,tags=["Login"])
def get_login(request:Request):
   return templates.TemplateResponse("login.html",{"request":request})


# #######################################################################
#
#                              CRUD DEVICES                             
#
#########################################################################

@app.post("/device",tags=["Device"])
def device(db:Session=Depends(get_db),
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
      

          
@app.get('/devices',response_model=List[schemas.Showdevice],  tags=["Device"])
def all(request:Request,db:Session = Depends(get_db) ):
       devices = db.query(models.Device).all()
       return templates.TemplateResponse("devices/show_device.html", {"request": request, "devices":devices})
      
      
@app.get('/device/{id}/edit',response_model=schemas.Showdevice,tags=["Device"])
def show(id,request:Request ,db:Session = Depends(get_db)):
      deviceshow = db.query(models.Device).filter(models.Device.id == id).first()
     
      # if not device:
      #       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      return templates.TemplateResponse("devices/show_device.html", {"request": request, "deviceshow": deviceshow  })
      

@app.put('/device/{id}/name',status_code=status.HTTP_202_ACCEPTED,tags=["Device"])
def device_name(id,request: schemas.Device,db:Session = Depends(get_db)):
     projet = db.query(models.Device).filter(models.Device.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.put('/device/{id}/id_gw',status_code=status.HTTP_202_ACCEPTED,tags=["Device"])
def device_gw(id,request: schemas.Device,db:Session = Depends(get_db)):
     Device = db.query(models.Device).filter(models.Device.id == id)
     if not Device.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     Device.update(request)
     db.commit()
     return "update"



@app.delete('/device/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Device"])
def destroy(id,db:Session = Depends(get_db)):
      db.query(models.Device).filter(models.Device.id == id).delete()
      db.commit()
      return 'done'


# #######################################################################
#
#                              CRUD GATEWAYE
#
#########################################################################


@app.post("/gatewaye/",tags=["Gatewaye"])
def gatewaye(db:Session=Depends(get_db),
             gw_Name:str = Form(...),
             g_id:str = Form(...),
             projet_id:int = Form(...)):
      new_gw = models.Gatewaye(
            name = gw_Name,
            g_id = g_id,
            projet_id = projet_id)
      db.add(new_gw)
      db.commit()      
      return RedirectResponse(url="/gatewayes", status_code=HTTP_302_FOUND)
      
@app.get('/gatewayes',response_model=List[schemas.Showgw],  tags=["Gatewaye"])
def all(request:Request,db:Session = Depends(get_db) ):
       gw = db.query(models.Gatewaye).all()
       return templates.TemplateResponse("gatewayes/show_gw.html", {"request": request, "gw": gw})


@app.get('/gatewaye/{id}',status_code=200,response_model=schemas.Showgw,tags=["Gatewaye"])
def gatewaye(id,request:Request ,db:Session = Depends(get_db)):
      gw = db.query(models.Gatewaye).filter(models.Gatewaye.id == id).first()
      if not gw:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      # return templates.TemplateResponse("projet.html", {"request": request, "gw": gw  })
      return gw

 
@app.put('/gatewaye/{id}/name',status_code=status.HTTP_202_ACCEPTED,tags=["Gatewaye"])
def gw_name(id,request: schemas.Projet,db:Session = Depends(get_db)):
     projet = db.query(models.Projet).filter(models.Projet.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"

@app.put('/gatewaye/{id}/name',status_code=status.HTTP_202_ACCEPTED,tags=["Gatewaye"])
def gw_name(id,request: schemas.Projet,db:Session = Depends(get_db)):
     projet = db.query(models.Projet).filter(models.Projet.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


# #######################################################################
#
#                              CRUD SENSORS
#
#########################################################################

@app.post("/sensor",tags=["Sensor"])
def sensor(db:Session=Depends(get_db),
           sensor_name:str = Form(...),
           unit:str=Form(...),
           type_sensor:str = Form(...),
           device_id:int = Form(...),
           s_id:str = Form(...)
           ):
      new_sensor = models.Sensor(
            sensor_name=sensor_name,
            unit=unit,
            type_sensor=type_sensor,
            device_id = device_id,
            s_id = s_id)
      

      db.add(new_sensor)
      db.commit()
      db.refresh(new_sensor)
      return RedirectResponse(url="/sensors", status_code=HTTP_302_FOUND)
            
             
@app.get('/sensors',response_model=List[schemas.Showsensor],  tags=["Sensor"])
def all(request:Request,db:Session = Depends(get_db) ):
       sensors = db.query(models.Sensor).all()
       return templates.TemplateResponse("sensors/show_sensor.html", {"request": request, "sensors": sensors})


@app.get('/sensor/{id}',status_code=200,response_model=schemas.Showsensor,tags=["Sensor"])
def show(id,request:Request ,db:Session = Depends(get_db)):
      projet = db.query(models.Sensor).filter(models.Sensor.id == id).first()
      if not projet:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      return templates.TemplateResponse("projet.html", {"request": request, "projets": projet  })

 
@app.put('/sensor/{id}/name',status_code=status.HTTP_202_ACCEPTED,tags=["Sensor"])
def sensor_name(id,request: schemas.Sensor,db:Session = Depends(get_db)):
     projet = db.query(models.Sensor).filter(models.Sensor.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.put('/sensor/{id}/id_device',status_code=status.HTTP_202_ACCEPTED,tags=["Sensor"])
def sensor_dvc(id,request: schemas.Sensor,db:Session = Depends(get_db)):
     projet = db.query(models.Sensor).filter(models.Sensor.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.delete('/sensor/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Sensor"])
def destroy(id,db:Session = Depends(get_db)):
      db.query(models.Sensor).filter(models.Sensor.id == id).delete()
      db.commit()
      return 'done'






