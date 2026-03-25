"""Tests for services layer.

Tests the medical service, cache service, and auth service.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.auth_service import auth_service
from src.services.medical_service import MedicalService
from src.models.schemas import DiagnosisRequest, TreatmentPlanRequest


class TestAuthService:
    """Tests for the authentication service."""

    def test_password_hash_and_verify(self) -> None:
        password = "REDACTED_TEST_PASSWORD"
        hashed = auth_service.hash_password(password)
        assert auth_service.check_password(password, hashed)

    def test_password_hash_different_each_time(self) -> None:
        password = "REDACTED_TEST_PASSWORD"
        hash1 = auth_service.hash_password(password)
        hash2 = auth_service.hash_password(password)
        assert hash1 != hash2

    def test_wrong_password_fails(self) -> None:
        hashed = auth_service.hash_password("REDACTED_TEST_PASSWORD")
        assert not auth_service.check_password("WrongPassword", hashed)

    def test_issue_token_returns_string(self) -> None:
        token = auth_service.issue_token("user123")
        assert isinstance(token, str)
        assert len(token) > 20

    def test_validate_password_strength_valid(self) -> None:
        valid, msg = auth_service.validate_password_strength("StrongP@ss1")
        assert valid is True
        assert msg == ""

    def test_validate_password_strength_too_short(self) -> None:
        valid, msg = auth_service.validate_password_strength("Ab1")
        assert valid is False
        assert "8 characters" in msg

    def test_validate_password_strength_no_uppercase(self) -> None:
        valid, msg = auth_service.validate_password_strength("lowercase1!")
        assert valid is False
        assert "uppercase" in msg


class TestMedicalService:
    """Tests for the medical service."""

    @pytest.fixture
    def service(self) -> MedicalService:
        return MedicalService()

    @pytest.mark.asyncio
    async def test_diagnose_returns_response(self, service: MedicalService) -> None:
        with patch.object(service, "model") as mock_model:
            mock_model.diagnose = AsyncMock(return_value={
                "diagnosis": "Test diagnosis",
                "confidence": 0.8,
            })
            mock_model.is_available = True
            service._model = mock_model
            service._cache = MagicMock()
            service._cache.get_json.return_value = None

            payload = DiagnosisRequest(symptoms=["fever", "cough"])
            result = await service.diagnose(payload)
            assert result.diagnosis == "Test diagnosis"
            assert result.confidence == 0.8

    @pytest.mark.asyncio
    async def test_treatment_plan_returns_response(self, service: MedicalService) -> None:
        with patch.object(service, "model") as mock_model:
            mock_model.generate_treatment_plan = AsyncMock(return_value={
                "treatment_plan": "Rest and fluids",
                "medications": [],
            })
            service._model = mock_model

            payload = TreatmentPlanRequest(diagnosis="Common cold")
            result = await service.generate_treatment_plan(payload)
            assert "treatment_plan" in result.model_dump()
# v29 - updated 2026-06-11
# v59 - updated 2026-06-11
