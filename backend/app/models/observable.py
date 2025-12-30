from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.database import Base

class Observable(Base):
    __tablename__ = "observables"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    value = Column(String)
    severity = Column(String)

class ObservableCreate(BaseModel):
    type: str  # ip | domain | hash
    value: str
