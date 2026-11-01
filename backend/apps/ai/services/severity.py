"""AI Emergency Severity Detection."""

CRITICAL_KEYWORDS = ["heart attack", "stroke", "unconscious", "not breathing", "cardiac", "severe bleeding"]
HIGH_KEYWORDS = ["accident", "fracture", "chest pain", "difficulty breathing"]


def calculate_severity(data: dict) -> dict:
    symptoms = (data.get("symptoms") or "").lower()
    voice_stress = data.get("voice_stress_score") or 0
    wearable = data.get("wearable_data") or {}
    heart_rate = wearable.get("heart_rate", 80)

    score = 0.5
    if any(k in symptoms for k in CRITICAL_KEYWORDS):
        score = 0.95
    elif any(k in symptoms for k in HIGH_KEYWORDS):
        score = 0.75

    if voice_stress > 0.7:
        score = min(1.0, score + 0.15)
    if heart_rate > 120 or heart_rate < 50:
        score = min(1.0, score + 0.2)

    if score >= 0.9:
        priority = "critical"
    elif score >= 0.7:
        priority = "high"
    elif score >= 0.5:
        priority = "medium"
    else:
        priority = "low"

    return {"score": round(score, 3), "priority": priority}
