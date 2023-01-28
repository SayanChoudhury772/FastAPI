from fastapi import FastAPI,Depends,status,HTTPException
from . import schemas,model
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import Union,Optional
import datetime
from datetime import date,timedelta

app= FastAPI()

model.Base.metadata.create_all(engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.post('/picks',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Pick,db:Session = Depends(get_db)):
    new_pick=model.Pick(title=request.title,tip=request.tip,odd=request.odd,event_date=request.event_date,comment=request.Comment)
    db.add(new_pick)
    db.commit()
    db.refresh(new_pick)
    return new_pick

@app.put('/picks/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request: schemas.Pick,db: Session=Depends(get_db)):
    new_pick = model.Pick(title=request.title,tip=request.tip,odd=request.odd,event_date=request.event_date,comment=request.Comment)
    pick=db.query(model.Pick).filter(model.Pick.id==id).update(new_pick,synchronize_session=False)
    """if not pick.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No picks are there for id = {id}")"""
    #pick.update(new_pick)
    #pick.update(request,synchronize_session=)
    #pick.update(request,synchronize_session=False)
    #picksofthatid(id,db).update(request)
    db.commit()
    return 'Updated'

@app.delete('/picks/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int,db: Session=Depends(get_db)):
    pick=db.query(model.Pick).filter(model.Pick.id==id)
    #pick=picksofthatid(id,db)
    if not pick.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No picks are there for id = {id}")
    pick.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

@app.get('/picks/all')
def all(db: Session=Depends(get_db)):
    picks= db.query(model.Pick).all()
    return picks

@app.get('/picks/',status_code=status.HTTP_302_FOUND)
def pickoftheday(date:Union[date,None] = date.today(),db: Session=Depends(get_db)):
    picks= db.query(model.Pick).filter(model.Pick.event_date==date).all()
    if not picks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No picks are there for date = {date}")
    return picks

@app.get('/picks/{id}',status_code=status.HTTP_302_FOUND)
def picksofthatid(id : int ,db: Session=Depends(get_db)):
    pick=db.query(model.Pick).filter(model.Pick.id==id).first()
    if not pick:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No picks are there for id = {id}")
    return pick
