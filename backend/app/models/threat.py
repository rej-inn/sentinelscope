from sqlalchemy import Column, Integer, String
from app.database import Base

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True)
    observable = Column(String, index=True)
    technique_id = Column(String)
    technique_name = Column(String)
