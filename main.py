from fastapi import FastAPI
from typing import Union,Optional
import datetime
from datetime import date,timedelta
from pydantic import BaseModel
class Pick(BaseModel):
    title : str
    tip : str
    odd : float
    event_date : date
    Comment : Union[str,None] = None


app = FastAPI()


@app.get('/')
def root():
    return "Hi, Welcome to Pickoflonewolf"

@app.get('/freepicks/')
def freepicks(date:Union[date,None] = date.today()):
    if date > (date.today()+timedelta(1)):
        return {"Thora sabar karle chutiye."}
    else:
        return {"Free picks of": date}

@app.post('/freepicks/')
def postpick(pick : Pick):
    return pick