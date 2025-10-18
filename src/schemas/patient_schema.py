from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str
    age: int


class PatientPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    patient_id: int
    name: str
    age: int


class PatientUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    name: str
    age: int
