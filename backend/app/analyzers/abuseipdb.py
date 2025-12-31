import os
import requests

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
BASE_URL = "https://api.abuseipdb.com/api/v2/check"

HEADERS = {
    "Accept": "application/json",
    "Key": API_KEY
}

def analyze(ip: str):
    if not API_KEY:
        return None

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    r = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
    if r.status_code != 200:
        return None

    data = r.json()["data"]
    score = data.get("abuseConfidenceScore", 0)

    if score >= 75:
        reputation = "malicious"
        severity = "malicious"
        confidence = score
    elif score >= 40:
        reputation = "suspicious"
        severity = "suspicious"
        confidence = score
    else:
        reputation = "clean"
        severity = "informational"
        confidence = score

    return {
        "source": "AbuseIPDB",
        "reputation": reputation,
        "severity": severity,
        "confidence": confidence
    }

