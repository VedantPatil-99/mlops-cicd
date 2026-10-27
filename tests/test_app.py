import unittest

from app import app
from model import predict_risk


class ModelTests(unittest.TestCase):
    def test_low_risk_prediction(self):
        result = predict_risk(10, 95, 88)
        self.assertEqual(result["risk_level"], "low")

    def test_high_risk_prediction(self):
        result = predict_risk(1, 40, 35)
        self.assertEqual(result["risk_level"], "high")


class RouteTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_prediction(self):
        response = self.client.get(
            "/predict?study_hours=8&attendance=90&previous_score=80"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.get_json()["risk_level"], {"low", "medium", "high"})

    def test_invalid_prediction(self):
        response = self.client.get(
            "/predict?study_hours=20&attendance=90&previous_score=80"
        )
        self.assertEqual(response.status_code, 400)

    def test_metrics(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"student_risk_prediction_requests_total", response.data)


if __name__ == "__main__":
    unittest.main()
