import traceback
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.exceptions.db_exceptions import NotFoundError
from src.schemas.note_schema import (
    NoteCreate,
    NotePublic,
    # NoteSearch,
    NoteSearchPublic,
    NoteUpdate,
)
from src.services import note_service

note_router = APIRouter(prefix="/notes")


@note_router.post("")
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
) -> NotePublic:
    try:
        return await note_service.create_note(db, note)
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.get("")
async def list_notes(
    db: AsyncSession = Depends(get_db),
    limit: Annotated[int, Query(le=100)] = 100,
    offset: int = 0,
) -> list[NotePublic]:
    try:
        return await note_service.list_notes(db, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.get("/{note_id}")
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)) -> NotePublic:
    try:
        return await note_service.get_note(db, note_id)
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
        return await note_service.update_note(db, note_id, note)
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
        await note_service.delete_note(db, note_id)
        return {"details": "note deleted"}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="note not found") from None
    except Exception as e:
        raise HTTPException(status_code=500) from e


@note_router.get("/search_notes/")
async def search(
    search_text: str, db: AsyncSession = Depends(get_db)
) -> list[NoteSearchPublic]:
    try:
        return await note_service.search_notes_by_text(db, search_text)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="note not found") from None
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500) from e
