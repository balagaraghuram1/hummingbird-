"""Pydantic schemas for API request/response models.

Defines type-safe data models for all API endpoints
with validation and documentation.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(description="Service status: ok, degraded, or error")
    service: str = Field(description="Service name")
    version: str = Field(default="1.0.0", description="Service version")
    ai_model: str = Field(default="unknown", description="AI model availability")
    cache: str = Field(default="unknown", description="Cache availability")


class DiagnosisRequest(BaseModel):
    """Diagnosis request model."""
    symptoms: list[str] = Field(
        min_length=1,
        max_length=20,
        description="List of patient symptoms",
        examples=[["fever", "cough", "fatigue"]],
    )
    patient_age: int | None = Field(default=None, ge=0, le=150)
    patient_sex: str | None = Field(default=None, pattern="^(male|female|other)$")


class DiagnosisResponse(BaseModel):
    """Diagnosis response model."""
    diagnosis: str = Field(description="Differential diagnosis")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    recommendations: list[str] = Field(default_factory=list)
    warning: str = Field(
        default="This is AI-generated analysis. Always consult a licensed physician.",
        description="Medical disclaimer",
    )


class TreatmentPlanRequest(BaseModel):
    """Treatment plan request model."""
    diagnosis: str = Field(min_length=1, max_length=2000)
    patient_age: int | None = Field(default=None, ge=0, le=150)
    patient_sex: str | None = Field(default=None, pattern="^(male|female|other)$")
    allergies: list[str] = Field(default_factory=list)
    current_medications: list[str] = Field(default_factory=list)


class TreatmentPlanResponse(BaseModel):
    """Treatment plan response model."""
    diagnosis: str
    treatment_plan: str
    medications: list[str] = Field(default_factory=list)
    lifestyle_changes: list[str] = Field(default_factory=list)
    follow_up: str = Field(default="Follow up with your healthcare provider")
    warning: str = Field(
        default="This is AI-generated guidance. Not a substitute for professional medical advice.",
        description="Medical disclaimer",
    )


class LabAnalysisRequest(BaseModel):
    """Lab analysis request model."""
    results: dict[str, float | str | int] = Field(
        min_length=1,
        description="Lab test results as name-value pairs",
        examples=[{"hemoglobin": 14.2, "glucose": 95, "cholesterol_total": 180}],
    )
    patient_age: int | None = Field(default=None, ge=0, le=150)
    patient_sex: str | None = Field(default=None, pattern="^(male|female|other)$")


class LabAnalysisResponse(BaseModel):
    """Lab analysis response model."""
    analysis: str = Field(description="Lab result interpretation")
    abnormal_values: list[dict] = Field(default_factory=list)
    total_tests: int = Field(default=0)
    recommendations: list[str] = Field(default_factory=list)
    warning: str = Field(
        default="This is AI-generated analysis. Consult your healthcare provider for confirmation.",
        description="Medical disclaimer",
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(description="Error message")
    error_code: str | None = Field(default=None)
# v14 - updated 2026-06-11
# v44 - updated 2026-06-11
