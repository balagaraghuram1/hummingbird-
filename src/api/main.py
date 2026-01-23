"""API router with all medical endpoints.

Defines REST API routes for diagnosis, treatment planning,
and lab analysis with proper error handling.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request

from src.core.exceptions import AIProviderError, ValidationError
from src.models.schemas import (
    DiagnosisRequest,
    DiagnosisResponse,
    ErrorResponse,
    HealthResponse,
    LabAnalysisRequest,
    LabAnalysisResponse,
    TreatmentPlanRequest,
    TreatmentPlanResponse,
)
from src.services.medical_service import medical_service

logger = logging.getLogger(__name__)

api_router = APIRouter()


@api_router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Monitoring"],
    summary="Service health check",
)
async def health() -> HealthResponse:
    """Check the health of the medical AI service.

    Returns the status of all components including the AI model,
    cache, and database connections.
    """
    return await medical_service.health_check()


@api_router.post(
    "/diagnose",
    response_model=DiagnosisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        503: {"model": ErrorResponse, "description": "AI provider unavailable"},
    },
    tags=["Medical AI"],
    summary="Generate medical diagnosis",
)
async def diagnose(payload: DiagnosisRequest) -> DiagnosisResponse:
    """Generate a differential diagnosis from patient symptoms.

    Analyzes the provided symptoms and returns a differential diagnosis
    with confidence score and recommendations.

    **Note**: This is AI-generated analysis. Always consult a licensed
    physician for definitive diagnosis.
    """
    try:
        return await medical_service.diagnose(payload)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except AIProviderError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        logger.error("Diagnosis endpoint error: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during diagnosis",
        ) from e


@api_router.post(
    "/treatment-plan",
    response_model=TreatmentPlanResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        503: {"model": ErrorResponse, "description": "AI provider unavailable"},
    },
    tags=["Medical AI"],
    summary="Generate treatment plan",
)
async def treatment_plan(payload: TreatmentPlanRequest) -> TreatmentPlanResponse:
    """Generate a treatment plan from a diagnosis.

    Creates a comprehensive treatment plan including medications,
    lifestyle changes, and follow-up recommendations.

    **Note**: This is AI-generated guidance. Not a substitute for
    professional medical advice.
    """
    try:
        return await medical_service.generate_treatment_plan(payload)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except AIProviderError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        logger.error("Treatment plan endpoint error: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during treatment plan generation",
        ) from e


@api_router.post(
    "/analyze-lab",
    response_model=LabAnalysisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        503: {"model": ErrorResponse, "description": "AI provider unavailable"},
    },
    tags=["Medical AI"],
    summary="Analyze laboratory results",
)
async def analyze_lab(payload: LabAnalysisRequest) -> LabAnalysisResponse:
    """Analyze laboratory test results.

    Interprets lab results, identifies abnormal values, and provides
    clinical significance assessments.

    **Note**: This is AI-generated analysis. Consult your healthcare
    provider for confirmation.
    """
    try:
        return await medical_service.analyze_lab_results(payload)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except AIProviderError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        logger.error("Lab analysis endpoint error: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during lab analysis",
        ) from e
# v4 - updated 2026-06-11
# v34 - updated 2026-06-11
# v64 - updated 2026-06-11
# v94 - updated 2026-06-11
# v124 - updated 2026-06-11
