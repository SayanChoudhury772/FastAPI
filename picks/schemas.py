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
    class Config:
        orm_mode = True