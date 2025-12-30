import os
import requests
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
BASE_URL = "https://www.virustotal.com/api/v3"
HEADERS = {"x-apikey": VT_API_KEY}


def vt_request(endpoint):
    r = requests.get(endpoint, headers=HEADERS, timeout=15)

    if r.status_code == 404:
        # Observable not known to VirusTotal
        return "NOT_FOUND"

    if r.status_code != 200:
        print(f"VT HTTP ERROR: {r.status_code}")
        return None

    return r.json()


def analyze(observable_type: str, value: str):
    try:
        if observable_type == "ip":
            url = f"{BASE_URL}/ip_addresses/{value}"
        elif observable_type == "domain":
            url = f"{BASE_URL}/domains/{value}"
        elif observable_type == "hash":
            url = f"{BASE_URL}/files/{value}"
        else:
            return None

        data = vt_request(url)

        # 🟡 Case: Not known to VirusTotal
        if data == "NOT_FOUND":
            return {
                "source": "VirusTotal",
                "reputation": "unknown",
                "severity": "informational",
                "confidence": 10
            }

        if not data:
            return None

        stats = data["data"]["attributes"].get("last_analysis_stats", {})
        print("VT stats:", stats)

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)

        if malicious > 0:
            return {
                "source": "VirusTotal",
                "reputation": "malicious",
                "severity": "malicious",
                "confidence": 90
            }

        if suspicious > 0:
            return {
                "source": "VirusTotal",
                "reputation": "suspicious",
                "severity": "suspicious",
                "confidence": 60
            }

        return {
            "source": "VirusTotal",
            "reputation": "clean",
            "severity": "low",
            "confidence": 30
        }

    except Exception as e:
        print("VT exception:", e)
        return None
