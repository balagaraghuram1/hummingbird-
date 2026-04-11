from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class DiagnosisRequest(BaseModel):
    symptoms: list[str] = Field(min_length=1)


class DiagnosisResponse(BaseModel):
    diagnosis: str
    confidence: float
    recommendations: list[str]


class TreatmentPlanRequest(BaseModel):
    diagnosis: str


class TreatmentPlanResponse(BaseModel):
    diagnosis: str
    treatment_plan: str

