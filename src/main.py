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
            
@app.get('/home',include_in_schema=False)
def home(request:Request):
      return templates.TemplateResponse('home.html',{"request":request})            
# #######################################################################
#
#  Route Formulaire Crèe Projets , Gatewayes, Devices, Sensors
#
#########################################################################
@app.get('/form_projet',tags=["Add"],include_in_schema=False)
def get_form(request:Request):
      return templates.TemplateResponse('/projets/add_projet.html',{"request":request})        

@app.get('/form_gw',tags=["Add"],response_model=List[schemas.Showprojet],include_in_schema=False)
def get_form(request:Request,db:Session=Depends(get_db)):
      projets = db.query(models.Projet).all()
      return templates.TemplateResponse('/gatewayes/add_gw.html',{"request":request,"projets":projets})  
    
@app.get('/form_device',tags=["Device"],response_model=List[schemas.Showdevice],include_in_schema=False)
def get_form(request:Request,db:Session=Depends(get_db)):
     
      gatewayes = db.query(models.Gatewaye).all()
   
      return templates.TemplateResponse("devices/add_device.html", {"request": request,
                                                                    "gatewaye": gatewayes,
                                                                    
                                                                    })


@app.get('/form_sensor',tags=["Add"],include_in_schema=False)
def get_form(request:Request,db:Session=Depends(get_db)):
       devices = db.query(models.Device).all()
       return templates.TemplateResponse('/sensors/add_sensor.html',{"request":request,"devices":devices})  


@app.get('/dashboard',tags=["Add"],include_in_schema=False)
def get_form(request:Request,db:Session=Depends(get_db)):
      #  devices = db.query(models.Device).all()
       return templates.TemplateResponse('dash.html',{"request":request})  




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
#                           CRUD PROJETS
#
#########################################################################

            
@app.post("/projet",tags=["Projets"])
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
            
       
@app.post("/projet/new",tags=["Projets"],include_in_schema=False)
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
      return new_projet
                 

@app.get('/projets/all',response_model=List[schemas.Showprojet], tags=["Projets"])
def get_all(request:Request,db:Session = Depends(get_db) ):
      projets = db.query(models.Projet).all()
      return projets

@app.get('/projets',response_model=List[schemas.Showprojet],  include_in_schema=False)
def all(request:Request,db:Session = Depends(get_db) ):
       projets = db.query(models.Projet).all()
       return templates.TemplateResponse("projets/show_projet.html", {"request": request, "projets": projets})
 


@app.get('/projet/{id}',status_code=200,response_model=schemas.Showprojet,include_in_schema=False)
def show(id,request:Request ,db:Session = Depends(get_db)):
      projet = db.query(models.Projet).filter(models.Projet.id == id).first()
      if not projet:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      # return templates.TemplateResponse("projet.html", {"request": request, "projets": projet  })
      return projet 

@app.put('/projet/{id}',status_code=status.HTTP_202_ACCEPTED,include_in_schema=False)
def update(id,request: schemas.Projet,db:Session = Depends(get_db)):
     projet = db.query(models.Projet).filter(models.Projet.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.delete('/projet/{id}',status_code=status.HTTP_204_NO_CONTENT,include_in_schema=False)
def destroy(id,db:Session = Depends(get_db)):
      db.query(models.Projet).filter(models.Projet.id == id).delete()
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

# #######################################################################
#
#                              CRUD DEVICES       include_in_schema=False                      
#
#########################################################################

@app.post("/device",tags=["Device"])
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
      

@app.get('/device',response_model=List[schemas.Showdevice], tags=["Device"] )
def get_devices(request:Request,db:Session = Depends(get_db) ):
       devices = db.query(models.Device).all()
       return templates.TemplateResponse("devices/show_device.html", {"request": request, "devices":devices})
       
      
@app.get('/devices',response_model=List[schemas.Showdevice],include_in_schema=False )
def all(request:Request,db:Session = Depends(get_db) ):
       devices = db.query(models.Device).all()
      #  return templates.TemplateResponse("devices/show_device.html", {"request": request, "devices":devices})
       return devices
      
      
      
@app.get('/device/{device_id}',response_model=schemas.Showdevice,tags=["Device"])
def show(id,request:Request ,db:Session = Depends(get_db)):
      deviceshow = db.query(models.Device).filter(models.Device.id == id).first()
     
      # if not device:
      #       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      return templates.TemplateResponse("devices/show_device.html", {"request": request, "deviceshow": deviceshow  })
      

@app.put('/device/{device_id}/name',status_code=status.HTTP_202_ACCEPTED,tags=["Device"])
def update(id,request: schemas.Device,db:Session = Depends(get_db)):
     projet = db.query(models.Device).filter(models.Device.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.delete('/device/{device_id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Device"])
def destroy(id,db:Session = Depends(get_db)):
      db.query(models.Device).filter(models.Device.id == id).delete()
      db.commit()
      return 'done'


@app.put('/device/{device_id}/gatewaye_id',status_code=status.HTTP_202_ACCEPTED,tags=["Device"])
def update_gatewaye(id,request: schemas.Device,db:Session = Depends(get_db)):
     Device = db.query(models.Device).filter(models.Device.id == id)
     if not Device.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     Device.update(request)
     db.commit()
     return "update"

