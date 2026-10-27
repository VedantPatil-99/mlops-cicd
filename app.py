from __future__ import annotations

from threading import Lock

from flask import Flask, Response, jsonify, render_template, request

from model import FEATURE_LIMITS, predict_risk


app = Flask(__name__)

_metrics_lock = Lock()
_metrics = {
    "prediction_requests": 0,
    "high_risk_predictions": 0,
    "validation_errors": 0,
}


def _record(metric: str) -> None:
    with _metrics_lock:
        _metrics[metric] += 1


def _parse_features(source: dict[str, object]) -> dict[str, float]:
    values: dict[str, float] = {}
    for name, (minimum, maximum) in FEATURE_LIMITS.items():
        raw_value = source.get(name)
        if raw_value in (None, ""):
            raise ValueError(f"{name} is required")
        try:
            value = float(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name} must be numeric") from exc
        if not minimum <= value <= maximum:
            raise ValueError(f"{name} must be between {minimum} and {maximum}")
        values[name] = value
    return values


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/health")
def health() -> Response:
    return jsonify(status="healthy", service="student-risk-monitor")


@app.route("/predict", methods=["GET", "POST"])
def predict() -> tuple[Response, int] | Response:
    source = request.get_json(silent=True) if request.is_json else request.values
    try:
        features = _parse_features(source or {})
    except ValueError as exc:
        _record("validation_errors")
        return jsonify(error=str(exc)), 400

    result = predict_risk(**features)
    _record("prediction_requests")
    if result["risk_level"] == "high":
        _record("high_risk_predictions")
    return jsonify(features=features, **result)


@app.get("/metrics")
def metrics() -> Response:
    with _metrics_lock:
        snapshot = dict(_metrics)
    lines = [
        "# HELP student_risk_prediction_requests_total Valid prediction requests.",
        "# TYPE student_risk_prediction_requests_total counter",
        f"student_risk_prediction_requests_total {snapshot['prediction_requests']}",
        "# HELP student_risk_high_predictions_total High-risk predictions.",
        "# TYPE student_risk_high_predictions_total counter",
        f"student_risk_high_predictions_total {snapshot['high_risk_predictions']}",
        "# HELP student_risk_validation_errors_total Invalid prediction requests.",
        "# TYPE student_risk_validation_errors_total counter",
        f"student_risk_validation_errors_total {snapshot['validation_errors']}",
    ]
    return Response("\n".join(lines) + "\n", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
