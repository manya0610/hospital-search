from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    patient_id: int
    text: str = Field(min_length=3, max_length=1000)
    embedding: list[float] | None = []


class NotePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    note_id: int
    patient_id: int
    text: str


class NoteUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    patient_id: int | None = None
    text: str | None = Field(default=None, min_length=3, max_length=1000)
    embedding: list[float] | None = []


class NoteSearchPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    text: str
    similarity_score: float
    patient_id: int
    note_id: int
