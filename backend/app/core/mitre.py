"""
Simple MITRE ATT&CK mapping based on observable type
and VirusTotal reputation signals.
"""

MITRE_MAP = {
    "ip": [
        {"id": "T1071", "name": "Application Layer Protocol"},
        {"id": "T1046", "name": "Network Service Scanning"}
    ],
    "domain": [
        {"id": "T1568", "name": "Dynamic Resolution"},
        {"id": "T1071", "name": "Application Layer Protocol"}
    ],
    "hash": [
        {"id": "T1059", "name": "Command and Scripting Interpreter"},
        {"id": "T1204", "name": "User Execution"}
    ]
}

def map_to_mitre(observable_type: str, reputation: str):
    if reputation in ["malicious", "suspicious"]:
        return MITRE_MAP.get(observable_type, [])
    return []
