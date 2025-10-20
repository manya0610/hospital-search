from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str = Field(min_length=3, max_length=50)
    age: int = Field(le=120, ge=0)


class PatientPublic(PatientCreate):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    patient_id: int


class PatientUpdate(PatientCreate):
    ...
