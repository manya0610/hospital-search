"""
Module serves as a wrapper over notes_repo.

We can extra business logic, or redis caching logic etc in here
mostly needed for update and search part
"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Note
from src.repo import note_repo
from src.schemas.note_schema import NoteCreate, NoteSearch, NoteSearchPublic, NoteUpdate
from src.services.embedding_model import get_embeddings


async def create_note(db: AsyncSession, note: NoteCreate) -> Note:
    note.embedding = get_embeddings(note.text)
    return await note_repo.create_note(db, note)


async def get_note(db: AsyncSession, note_id: int) -> Note:
    return await note_repo.get_note(db, note_id)


async def list_notes(db: AsyncSession, limit: int = 100, offset: int = 0) -> list[Note]:
    return await note_repo.list_notes(db, limit, offset)


async def update_note(db: AsyncSession, note_id: int, note: NoteUpdate) -> Note:
    """
    Update Note

    We remove attributes that are not set, incase user didn't pass those in json
    This avoids setting null values for not passed fields.
    """
    if note.text is None:
        delattr(note, "text")
    else:
        note.embedding = get_embeddings(note.text)

    if note.patient_id is None:
        delattr(note, "patient_id")

    return await note_repo.update_note(db, note_id, note)


async def delete_note(db: AsyncSession, note_id: int) -> Note:
    return await note_repo.delete_note(db, note_id)


async def search_notes_by_text(
    db: AsyncSession, search_note: NoteSearch
) -> list[NoteSearchPublic]:
    """
    Semantic search over text

    Creates embedding from text and searches notes using that embedding.
    """
    embedding = get_embeddings(search_note.text)
    notes: list[tuple[Note, float]] = await note_repo.search_notes_by_text_vector(
        db, embedding
    )
    # adding similarity score to NoteSearchPublic model,
    # because `note_repo.search_notes_by_text_vector` returns note with similarity score
    return [
        NoteSearchPublic(**note.__dict__, similarity_score=similarity_score)
        for (note, similarity_score) in notes
    ]
