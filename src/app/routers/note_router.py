import traceback
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.database.models import Note
from src.exceptions.db_exceptions import NotFoundError
from src.repo import note_repo
from src.schemas.note_schema import (
    NoteCreate,
    NotePublic,
    NoteSearch,
    NoteSearchPublic,
    NoteUpdate,
)

note_router = APIRouter(prefix="/note")


@note_router.post("")
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
) -> NotePublic:
    try:
        note: Note = await note_repo.create_note(db, note)
        return note
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.get("")
async def list_notes(
    db: AsyncSession = Depends(get_db),
    limit: Annotated[int, Query(le=100)] = 100,
    offset: int = 0,
) -> list[NotePublic]:
    try:
        notes: list[Note] = await note_repo.list_notes(db, limit, offset)
        return notes
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.get("/{note_id}")
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)) -> NotePublic:
    try:
        note: Note = await note_repo.get_note(db, note_id)
        return note
    except NotFoundError:
        raise HTTPException(status_code=404, detail="note not found") from None
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.patch("/{note_id}")
async def update_note(
    note_id: int,
    note: NoteUpdate,
    db: AsyncSession = Depends(get_db),
) -> NotePublic:
    try:
        note: Note = await note_repo.update_note(db, note_id, note)
        return note
    except NotFoundError:
        raise HTTPException(status_code=404, detail="note not found") from None
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    try:
        await note_repo.delete_note(db, note_id)
        return {"details": "note deleted"}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="note not found") from None
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.post("/search")
async def search(
    search_note: NoteSearch, db: AsyncSession = Depends(get_db)
) -> list[NoteSearchPublic]:
    try:
        notes: list[tuple[Note, float]] = await note_repo.search_notes(
            db, search_note.text
        )

        return [
            NoteSearchPublic(**note.__dict__, similarity_score=similarity_score)
            for (note, similarity_score) in notes
        ]
    except NotFoundError:
        raise HTTPException(status_code=404, detail="note not found") from None
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500) from e
