from .database import Base
from sqlalchemy import Column,Integer,String,Float,Date

class Pick(Base):
    __tablename__='Picks'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    tip=Column(String)
    odd=Column(Float)
    event_date=Column(Date)
    comment=Column(String,nullable=True)

    