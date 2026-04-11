from src.medical_ai.model import MedicalAIModel
from src.models.schemas import (
    DiagnosisRequest,
    DiagnosisResponse,
    TreatmentPlanRequest,
    TreatmentPlanResponse,
)
from src.services.cache_service import cache_service


class MedicalService:
    def __init__(self) -> None:
        self.model = MedicalAIModel()

    async def diagnose(self, payload: DiagnosisRequest) -> DiagnosisResponse:
        cache_key = f"diagnose:{'|'.join(payload.symptoms)}"
        cached = cache_service.get_json(cache_key)
        if cached:
            return DiagnosisResponse(**cached)

        result = await self.model.diagnose(payload.symptoms)
        response = DiagnosisResponse(
            diagnosis=result.get("diagnosis", "No diagnosis available"),
            confidence=0.78,
            recommendations=["Consult a licensed physician"],
        )
        cache_service.set_json(cache_key, response.model_dump())
        return response

    async def generate_treatment_plan(
        self, payload: TreatmentPlanRequest
    ) -> TreatmentPlanResponse:
        result = await self.model.generate_treatment_plan(payload.diagnosis)
        return TreatmentPlanResponse(
            diagnosis=payload.diagnosis,
            treatment_plan=result.get("treatment_plan", "No treatment plan available"),
        )


medical_service = MedicalService()

