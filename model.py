from __future__ import annotations


FEATURE_LIMITS = {
    "study_hours": (0.0, 12.0),
    "attendance": (0.0, 100.0),
    "previous_score": (0.0, 100.0),
}


def predict_risk(
    study_hours: float,
    attendance: float,
    previous_score: float,
) -> dict[str, float | str]:
    """Return a transparent student-performance risk estimate.

    The scoring rule is intentionally deterministic so the lab focuses on
    CI/CD and monitoring rather than model training.
    """
    readiness = (
        (study_hours / 12.0) * 0.30
        + (attendance / 100.0) * 0.35
        + (previous_score / 100.0) * 0.35
    )
    risk_score = round(max(0.0, min(1.0, 1.0 - readiness)), 3)
    if risk_score >= 0.55:
        risk_level = "high"
    elif risk_score >= 0.30:
        risk_level = "medium"
    else:
        risk_level = "low"
    return {"risk_score": risk_score, "risk_level": risk_level}
