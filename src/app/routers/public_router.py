import traceback
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.exceptions.db_exceptions import NotFoundError
from src.schemas.note_schema import (
    NoteCreate,
    NotePublic,
    NoteSearchPublic,
)
from src.services import note_service

public_router = APIRouter(prefix="")


@public_router.get("/search_notes")
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


@public_router.post("/add_note")
async def add_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
) -> NotePublic:
    try:
        return await note_service.create_note(db, note)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500) from e
