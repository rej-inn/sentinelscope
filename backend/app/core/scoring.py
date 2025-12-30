def calculate_score(results):
    """
    Calculate average confidence score from enrichment results.
    Ignores failed or None enrichments.
    """

    valid = [
        r.get("confidence", 0)
        for r in results
        if isinstance(r, dict) and "confidence" in r
    ]

    if not valid:
        return 0

    # Use real average, not integer truncation
    return int(sum(valid) / len(valid))
