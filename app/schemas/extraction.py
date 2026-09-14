from pydantic import BaseModel, Field


class MedicalExtraction(BaseModel):
    patient_name: str | None = None
    age: int | None = None

    diagnoses: list[str] = Field(default_factory=list)

    bmi: float | None = None

    smoker: bool | None = None

    blood_pressure: str | None = None