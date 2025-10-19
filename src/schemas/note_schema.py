from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    patient_id: int
    text: str
    embedding: list[float] | None = Field(default=None, exclude=True)


class NotePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    note_id: int
    patient_id: int
    text: str


class NoteUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    patient_id: int | None = None
    text: str | None = None
    embedding: list[float] | None = Field(default=None, exclude=True)


class NoteSearchPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    text: str
    similarity_score: float
    patient_id: int
    note_id: int
