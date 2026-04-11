from fastapi import APIRouter, HTTPException

from src.models.schemas import (
    DiagnosisRequest,
    DiagnosisResponse,
    HealthResponse,
    TreatmentPlanRequest,
    TreatmentPlanResponse,
)
from src.services.medical_service import medical_service


api_router = APIRouter()


@api_router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="hummingbird-medical-ai")


@api_router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(payload: DiagnosisRequest) -> DiagnosisResponse:
    try:
        return await medical_service.diagnose(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@api_router.post("/treatment-plan", response_model=TreatmentPlanResponse)
async def treatment_plan(payload: TreatmentPlanRequest) -> TreatmentPlanResponse:
    try:
        return await medical_service.generate_treatment_plan(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

