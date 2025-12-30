def determine_severity(score: int):
    if score >= 80:
        return "Malicious"
    if score >= 50:
        return "Suspicious"
    return "Informational"
