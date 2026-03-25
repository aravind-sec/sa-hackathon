def calculate_risk(alerts):
    risk_score = 0

    for alert in alerts:
        if alert["attack_type"] == "Credential Stuffing":
            risk_score += 40
        elif alert["attack_type"] == "Rate Abuse":
            risk_score += 30
        elif alert["attack_type"] == "Suspicious Endpoint Access":
            risk_score += 20

    # ---------- Risk Level ----------
    if risk_score >= 70:
        level = "HIGH"
    elif risk_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return risk_score, level