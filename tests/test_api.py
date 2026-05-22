"""Tests for API endpoints.

Tests the FastAPI API routes for health, diagnosis,
treatment, and lab analysis endpoints.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from src.main import app


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client: TestClient) -> None:
        response = client.get("/api/health")
        data = response.json()
        assert "status" in data
        assert data["service"] == "hummingbird-medical-ai"

    def test_health_includes_version(self, client: TestClient) -> None:
        response = client.get("/api/health")
        data = response.json()
        assert "version" in data


class TestDiagnoseEndpoint:
    """Tests for the diagnosis endpoint."""

    def test_diagnose_returns_200(self, client: TestClient, sample_symptoms: list[str]) -> None:
        with patch("src.services.medical_service.medical_service.diagnose") as mock:
            mock.return_value = AsyncMock(
                diagnosis="Test diagnosis",
                confidence=0.8,
                recommendations=["Consult physician"],
            )
            response = client.post(
                "/api/diagnose",
                json={"symptoms": sample_symptoms},
            )
            assert response.status_code == 200

    def test_diagnose_rejects_empty_symptoms(self, client: TestClient) -> None:
        response = client.post("/api/diagnose", json={"symptoms": []})
        assert response.status_code == 422

    def test_diagnose_rejects_missing_symptoms(self, client: TestClient) -> None:
        response = client.post("/api/diagnose", json={})
        assert response.status_code == 422


class TestTreatmentPlanEndpoint:
    """Tests for the treatment plan endpoint."""

    def test_treatment_plan_returns_200(self, client: TestClient, sample_diagnosis: str) -> None:
        with patch("src.services.medical_service.medical_service.generate_treatment_plan") as mock:
            mock.return_value = AsyncMock(
                diagnosis=sample_diagnosis,
                treatment_plan="Rest and hydration",
                medications=[],
                lifestyle_changes=[],
                follow_up="Follow up in 1 week",
            )
            response = client.post(
                "/api/treatment-plan",
                json={"diagnosis": sample_diagnosis},
            )
            assert response.status_code == 200

    def test_treatment_plan_rejects_empty_diagnosis(self, client: TestClient) -> None:
        response = client.post("/api/treatment-plan", json={"diagnosis": ""})
        assert response.status_code == 422


class TestLabAnalysisEndpoint:
    """Tests for the lab analysis endpoint."""

    def test_lab_analysis_returns_200(self, client: TestClient, sample_lab_results: dict) -> None:
        with patch("src.services.medical_service.medical_service.analyze_lab_results") as mock:
            mock.return_value = AsyncMock(
                analysis="All values normal",
                abnormal_values=[],
                recommendations=[],
            )
            response = client.post(
                "/api/analyze-lab",
                json={"results": sample_lab_results},
            )
            assert response.status_code == 200

    def test_lab_analysis_rejects_empty_results(self, client: TestClient) -> None:
        response = client.post("/api/analyze-lab", json={"results": {}})
        assert response.status_code == 422
# v28 - updated 2026-06-11
# v58 - updated 2026-06-11
# v88 - updated 2026-06-11
