from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.observable import ObservableCreate
from app.services.observable_service import process_observable

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def submit_observable(data: ObservableCreate, db: Session = Depends(get_db)):
    return process_observable(data, db)
