from app.analyzers import virustotal, abuseipdb, otx


def enrich(observable_type: str, value: str):
    """
    Enrich an observable using multiple threat intelligence sources.
    Returns a list of normalized enrichment results.
    """
    results = []

    # VirusTotal (IPs, domains, hashes)
    vt_result = virustotal.analyze(observable_type, value)
    if vt_result:
        results.append(vt_result)

    # IP-only enrichments
    if observable_type == "ip":
        abuse_result = abuseipdb.analyze(value)
        if abuse_result:
            results.append(abuse_result)

        otx_result = otx.analyze(value)
        if otx_result:
            results.append(otx_result)

    return results
