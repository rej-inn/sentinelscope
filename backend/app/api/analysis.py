from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.analysis_result import AnalysisResult
from app.services.mitre_service import get_mitre_by_observable

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def list_analysis(db: Session = Depends(get_db)):
    return db.query(AnalysisResult).all()

@router.get("/{observable}/mitre")
def get_mitre(observable: str, db: Session = Depends(get_db)):
    techniques = get_mitre_by_observable(observable, db)

    if not techniques:
        raise HTTPException(
            status_code=404,
            detail="No MITRE techniques found for this observable"
        )

    return {
        "observable": observable,
        "mitre_attack": techniques
    }
