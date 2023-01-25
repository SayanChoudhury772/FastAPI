from fastapi import FastAPI,Depends
from . import schemas,model
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

app= FastAPI()

model.Base.metadata.create_all(engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.post('/picks')
def create(request: schemas.Pick,db:Session = Depends(get_db)):
    new_pick=model.Pick(title=request.title,tip=request.tip,odd=request.odd,event_date=request.event_date,comment=request.Comment)
    db.add(new_pick)
    db.commit()
    db.refresh(new_pick)
    return new_pick

@app.get('/picks/all')
def all(db: Session=Depends(get_db)):
    picks= db.query(model.Pick).all()
    return picks
