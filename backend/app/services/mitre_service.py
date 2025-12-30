from sqlalchemy.orm import Session
from app.models.threat import Threat

def get_mitre_by_observable(observable: str, db: Session):
    results = (
        db.query(Threat)
        .filter(Threat.observable == observable)
        .all()
    )

    return [
        {
            "id": r.technique_id,
            "name": r.technique_name
        }
        for r in results
    ]
