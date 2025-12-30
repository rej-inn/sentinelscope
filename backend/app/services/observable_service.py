from app.core.enrichment import enrich
from app.core.scoring import calculate_score
from app.core.correlation import determine_severity
from app.core.mitre import map_to_mitre
from app.models.observable import Observable
from app.models.analysis_result import AnalysisResult
from app.models.threat import Threat


def process_observable(data, db):
    # 1️⃣ Run enrichment
    enrichment_results = enrich(data.type, data.value) or []

    # 2️⃣ Keep ONLY valid enrichment results
    valid_enrichments = [
        r for r in enrichment_results
        if isinstance(r, dict) and "confidence" in r
    ]

    # 3️⃣ Calculate score ONLY from valid data
    score = calculate_score(valid_enrichments)
    severity = determine_severity(score)

    # 4️⃣ Store observable
    observable = Observable(
        type=data.type,
        value=data.value,
        severity=severity
    )
    db.add(observable)
    db.commit()

    mitre_techniques = []

    # 5️⃣ Store analysis results
    for r in valid_enrichments:
        result = AnalysisResult(
            observable_value=data.value,
            source=r.get("source"),
            reputation=r.get("reputation", "unknown"),
            confidence=r.get("confidence", 0)
        )
        db.add(result)

        mapped = map_to_mitre(data.type, r.get("reputation"))
        for t in mapped:
            threat = Threat(
                observable=data.value,
                technique_id=t["id"],
                technique_name=t["name"]
            )
            db.add(threat)
            mitre_techniques.append(t)

    db.commit()

    # 6️⃣ Return API response
    return {
        "observable": data.value,
        "type": data.type,
        "severity": severity,
        "confidence": score,
        "mitre_attack": mitre_techniques,
        "enrichment": valid_enrichments
    }
