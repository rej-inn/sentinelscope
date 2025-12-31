import os
import requests

API_KEY = os.getenv("OTX_API_KEY")

BASE_URL = "https://otx.alienvault.com/api/v1/indicators/IPv4"

HEADERS = {
    "X-OTX-API-KEY": API_KEY
}


def analyze(ip: str):
    """
    AlienVault OTX IP reputation lookup
    """

    if not API_KEY:
        return {
            "source": "AlienVault OTX",
            "error": "API key not configured"
        }

    try:
        url = f"{BASE_URL}/{ip}/general"
        resp = requests.get(url, headers=HEADERS, timeout=10)

        if resp.status_code != 200:
            return {
                "source": "AlienVault OTX",
                "error": f"HTTP {resp.status_code}"
            }

        data = resp.json()

        pulse_info = data.get("pulse_info", {})
        pulse_count = pulse_info.get("count", 0)

        # 🔍 SOC-tuned thresholds
        if pulse_count >= 3:
            reputation = "malicious"
            confidence = 85
        elif pulse_count >= 1:
            reputation = "suspicious"
            confidence = 60
        else:
            reputation = "clean"
            confidence = 20

        return {
            "source": "AlienVault OTX",
            "reputation": reputation,
            "confidence": confidence,
            "pulse_count": pulse_count
        }

    except Exception as e:
        return {
            "source": "AlienVault OTX",
            "error": str(e)
        }
