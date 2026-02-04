"""Medical service layer.

Handles business logic for medical AI operations including
diagnosis, treatment recommendations, and lab analysis.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.core.exceptions import AIProviderError, ServiceUnavailableError
from src.models.schemas import (
    DiagnosisRequest,
    DiagnosisResponse,
    HealthResponse,
    LabAnalysisRequest,
    LabAnalysisResponse,
    TreatmentPlanRequest,
    TreatmentPlanResponse,
)

if TYPE_CHECKING:
    from src.medical_ai.model import MedicalAIModel

logger = logging.getLogger(__name__)


class MedicalService:
    """Service for medical AI operations.

    Provides diagnosis, treatment planning, and lab analysis
    with caching and error handling.
    """

    def __init__(self) -> None:
        self._model: MedicalAIModel | None = None
        self._cache = None

    @property
    def model(self) -> "MedicalAIModel":
        """Lazy-load the medical AI model."""
        if self._model is None:
            from src.medical_ai.model import medical_ai_model
            self._model = medical_ai_model
        return self._model

    @property
    def cache(self):
        """Lazy-load the cache service."""
        if self._cache is None:
            try:
                from src.services.cache_service import cache_service
                self._cache = cache_service
            except Exception:
                logger.warning("Cache service unavailable")
        return self._cache

    async def diagnose(self, payload: DiagnosisRequest) -> DiagnosisResponse:
        """Generate a diagnosis from patient symptoms.

        Args:
            payload: Diagnosis request with patient symptoms.

        Returns:
            Diagnosis response with differential diagnosis.

        Raises:
            AIProviderError: If the AI provider fails.
        """
        cache_key = f"diagnose:{'|'.join(sorted(payload.symptoms))}"

        if self.cache:
            cached = self.cache.get_json(cache_key)
            if cached:
                logger.info("Cache hit for diagnosis: %s", cache_key)
                return DiagnosisResponse(**cached)

        try:
            result = await self.model.diagnose(payload.symptoms)
        except Exception as e:
            logger.error("Diagnosis failed: %s", e)
            raise AIProviderError(f"Diagnosis generation failed: {e}") from e

        response = DiagnosisResponse(
            diagnosis=result.get("diagnosis", "No diagnosis available"),
            confidence=result.get("confidence", 0.0),
            recommendations=result.get("recommendations", ["Consult a licensed physician"]),
        )

        if self.cache:
            try:
                self.cache.set_json(cache_key, response.model_dump())
            except Exception as e:
                logger.warning("Failed to cache diagnosis: %s", e)

        return response

    async def generate_treatment_plan(
        self, payload: TreatmentPlanRequest
    ) -> TreatmentPlanResponse:
        """Generate a treatment plan from a diagnosis.

        Args:
            payload: Treatment plan request with diagnosis.

        Returns:
            Treatment plan response.

        Raises:
            AIProviderError: If the AI provider fails.
        """
        try:
            result = await self.model.generate_treatment_plan(payload.diagnosis)
        except Exception as e:
            logger.error("Treatment plan generation failed: %s", e)
            raise AIProviderError(f"Treatment plan generation failed: {e}") from e

        return TreatmentPlanResponse(
            diagnosis=payload.diagnosis,
            treatment_plan=result.get("treatment_plan", "No treatment plan available"),
            medications=result.get("medications", []),
            lifestyle_changes=result.get("lifestyle_changes", []),
            follow_up=result.get("follow_up", "Follow up with your healthcare provider"),
        )

    async def analyze_lab_results(
        self, payload: LabAnalysisRequest
    ) -> LabAnalysisResponse:
        """Analyze laboratory test results.

        Args:
            payload: Lab analysis request with test results.

        Returns:
            Lab analysis response with interpretations.

        Raises:
            AIProviderError: If the AI provider fails.
        """
        try:
            result = await self.model.analyze_lab_results(payload.results)
        except Exception as e:
            logger.error("Lab analysis failed: %s", e)
            raise AIProviderError(f"Lab analysis failed: {e}") from e

        return LabAnalysisResponse(
            analysis=result.get("analysis", "No analysis available"),
            abnormal_values=result.get("abnormal_values", []),
            recommendations=result.get("recommendations", []),
        )

    async def health_check(self) -> HealthResponse:
        """Perform a health check of the medical service.

        Returns:
            Health status response.
        """
        model_status = "available" if self.model.is_available else "unavailable"
        cache_status = "available"
        if self.cache:
            try:
                self.cache.get_json("__health_check__")
            except Exception:
                cache_status = "unavailable"

        overall_status = "ok" if model_status == "available" else "degraded"

        return HealthResponse(
            status=overall_status,
            service="hummingbird-medical-ai",
            version="1.0.0",
            ai_model=model_status,
            cache=cache_status,
        )


medical_service = MedicalService()
# v7 - updated 2026-06-11
# v37 - updated 2026-06-11
# v67 - updated 2026-06-11
# v97 - updated 2026-06-11
# v127 - updated 2026-06-11
