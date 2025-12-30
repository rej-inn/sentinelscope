from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    observable_value = Column(String, index=True)
    source = Column(String)
    reputation = Column(String)
    confidence = Column(Integer)
