from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class Note(Base):
    __tablename__ = "notes"
    note_id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.patient_id"))
    text: Mapped[str] = mapped_column(nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))  # size must match model
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


notes_embedding_idx = Index(
    "notes_embedding_idx",  # index name
    Note.embedding,
    postgresql_using="ivfflat",
    postgresql_ops={"embedding": "vector_cosine_ops"},
    postgresql_with={"lists": 100},  # tuning parameter
)
