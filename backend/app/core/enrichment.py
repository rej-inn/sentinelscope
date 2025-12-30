from app.analyzers import virustotal, abuseipdb

def enrich(observable_type: str, value: str):
    results = []

    # VirusTotal (all types)
    results.append(virustotal.analyze(observable_type, value))

    # AbuseIPDB only for IPs
    if observable_type == "ip":
        results.append(abuseipdb.analyze(value))

    return results
