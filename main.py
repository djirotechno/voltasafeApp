from typing import Optional,List

from fastapi import FastAPI, Request,Depends,status,Form
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.utils.decor import deprecated_function
from sqlalchemy.sql.expression import false
from starlette.responses import Response
import schemas,models
from database import SessionLocal, engine
from sqlalchemy.orm import Session, session 
import token_0
from hashing import Hash
import oauth2
from fastapi.security import OAuth2PasswordRequestForm

  # ,get_current_user:schemas.User = Depends(oauth2.get_current_user)

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
            
            
@app.post("/projet/",tags=["Projets"])
def project(request:schemas.Projet,db:Session=Depends(get_db)):
      new_projet = models.Projet(
            typepv=request.typepv,
            vmx=request.vmx,
            imx=request.imx,
            pmx=request.pmx,
            temp=request.temp,
            long=request.long,
            lat=request.lat,
            user_id = 1)

      db.add(new_projet)
      db.commit()
      db.refresh(new_projet)
      return new_projet
            
            
            
          
@app.get('/projet',response_model=List[schemas.Showprojet],  tags=["Projets"])
def all(request:Request,db:Session = Depends(get_db) ):
       projets = db.query(models.Projet).all()
       return templates.TemplateResponse("projet.html", {"request": request, "projets": projets})




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

 
# @app.get('/new_projet',response_class=HTMLResponse,tags=["Login"])
# def get_login(request:Request):
#    return templates.TemplateResponse("create_projet.html",{"request":request})


# LOGIN

@app.post('/login',tags=["Login"])
def login(request:OAuth2PasswordRequestForm = Depends(), email: str = Form(...),db:Session=Depends(get_db)):
      user = db.query(models.User).filter(models.User.email == request.username).first()
      if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Creentials")
      if not Hash.verifie(user.password,request.password):
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrecte Password")
      access_token = token_0.create_access_token(data={"sub": user.email})
      
      return templates.TemplateResponse("home.html", {"request": request})
      





# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("home.html", {"request": request, "id": id})










@app.post("/device/",tags=["Device"])
def device(request:schemas.Device,db:Session=Depends(get_db)):
      new_dev = models.Device(
            name=request.name,
            gw_id = 1)

      db.add(new_dev)
      db.commit()
      db.refresh(new_dev)
      return new_dev
            
            
            
          
@app.get('/devices',response_model=List[schemas.Showdevice],  tags=["Device"])
def all(request:Request,db:Session = Depends(get_db) ):
       devices = db.query(models.Device).all()
      #  return templates.TemplateResponse("projet.html", {"request": request, "projets": projets})
      
       return devices




@app.get('/device/{id}',status_code=200,response_model=schemas.Showdevice,tags=["Device"])
def show(id,request:Request ,db:Session = Depends(get_db)):
      device = db.query(models.Device).filter(models.Device.id == id).first()
      if not device:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      # return templates.TemplateResponse("projet.html", {"request": request, "projets": projet  })
      return device

 


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









@app.post("/gateway/",tags=["Gatewaye"])
def gatewaye(request:schemas.Gatewaye,db:Session=Depends(get_db)):
      new_gw = models.Gatewaye(
            name=request.name,
            projet_id = 1)

      db.add(new_gw)
      db.commit()
      db.refresh(new_gw)
      return new_gw
            
            
            
          
@app.get('/gatewayes',response_model=List[schemas.Showgw],  tags=["Gatewaye"])
def all(request:Request,db:Session = Depends(get_db) ):
       gw = db.query(models.Gatewaye).all()
       
       return gw
      #  return templates.TemplateResponse("projet.html", {"request": request, "projets": projets})




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












@app.post("/sensor/",tags=["Sensor"])
def sensor(request:schemas.Projet,db:Session=Depends(get_db)):
      new_projet = models.Projet(
            typepv=request.typepv,
            vmx=request.vmx,
            imx=request.imx,
            pmx=request.pmx,
            temp=request.temp,
            long=request.long,
            lat=request.lat,
            user_id = 1)

      db.add(new_projet)
      db.commit()
      db.refresh(new_projet)
      return new_projet
            
            
            
          
@app.get('/sensor',response_model=List[schemas.Showprojet],  tags=["Sensor"])
def all(request:Request,db:Session = Depends(get_db) ):
       projets = db.query(models.Projet).all()
       return templates.TemplateResponse("projet.html", {"request": request, "projets": projets})




@app.get('/sensor/{id}',status_code=200,response_model=schemas.Showprojet,tags=["Sensor"])
def show(id,request:Request ,db:Session = Depends(get_db)):
      projet = db.query(models.Projet).filter(models.Projet.id == id).first()
      if not projet:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
      return templates.TemplateResponse("projet.html", {"request": request, "projets": projet  })

 

@app.put('/sensor/{id}/name',status_code=status.HTTP_202_ACCEPTED,tags=["Sensor"])
def sensor_name(id,request: schemas.Projet,db:Session = Depends(get_db)):
     projet = db.query(models.Projet).filter(models.Projet.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.put('/sensor/{id}/id_device',status_code=status.HTTP_202_ACCEPTED,tags=["Sensor"])
def sensor_dvc(id,request: schemas.Projet,db:Session = Depends(get_db)):
     projet = db.query(models.Projet).filter(models.Projet.id == id)
     if not projet.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Projet with id {id} is not available")
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {'detail':f"Projet with id {id} is not available"}
     projet.update(request)
     db.commit()
     return "update"


@app.delete('/sensor/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["Sensor"])
def destroy(id,db:Session = Depends(get_db)):
      db.query(models.Projet).filter(models.Projet.id == id).delete()
      db.commit()
      return 'done'






