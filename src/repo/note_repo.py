import logging
from collections.abc import Sequence

from sqlalchemy import CursorResult, ScalarResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from torch import Tensor

from src.database.models import Note
from src.exceptions.db_exceptions import DatabaseError, NotFoundError
from src.schemas.note_schema import NoteCreate, NoteUpdate

logging.basicConfig()
logger = logging.getLogger(__name__)


async def create_note(session: AsyncSession, note: NoteCreate) -> Note:
    try:
        query = insert(Note).values(note.model_dump()).returning(Note)
        note: Note = await session.scalar(query)
        await session.commit()
        return note
    except Exception as e:
        await session.rollback()
        logger.exception("Error creating note=%s", note, stack_info=True)
        raise DatabaseError from e


async def get_note(session: AsyncSession, note_id: int) -> Note:
    try:
        query = select(Note).where(Note.note_id == note_id)
        result: ScalarResult = await session.scalars(query)
        note = result.one_or_none()
        if note is None:
            logger.exception("note with id=%s not found", note_id, stack_info=True)
            raise NotFoundError
        return note
    except NotFoundError:
        raise
    except Exception as e:
        logger.exception(
            "Error while getting note with id=%s",
            note_id,
            stack_info=True,
        )
        raise DatabaseError from e


# List all note, returning a list of Note objects
async def list_notes(session: AsyncSession, limit: int, offset: int) -> list[Note]:
    try:
        query = select(Note).limit(limit).offset(offset)
        response: ScalarResult = await session.scalars(query)
        notes: Sequence[Note] = response.all()
        return notes
    except Exception as e:
        logger.exception("Error while listing note", stack_info=True)
        raise DatabaseError from e


async def update_note(session: AsyncSession, note_id: int, note: NoteUpdate) -> Note:
    try:
        query = (
            update(Note)
            .where(Note.note_id == note_id)
            .values(**note.model_dump())
            .returning(Note)
        )
        note: Note = await session.scalar(query)
        await session.commit()
        if note is None:
            logger.warning("No note found with id=%s to update", note_id)
            raise NotFoundError
        return note
    except NotFoundError:
        raise
    except Exception as e:
        await session.rollback()
        logger.exception(
            "Error updating note with id=%s, data=%s",
            note_id,
            note,
            stack_info=True,
        )
        raise DatabaseError from e


async def delete_note(session: AsyncSession, note_id: int) -> int:
    try:
        query = delete(Note).where(Note.id == note_id)
        response: CursorResult = await session.execute(query)
        await session.commit()

        if response.rowcount == 0:
            logger.warning("No note found with id=%s to delete", note_id)
            raise NotFoundError
        return response.rowcount
    except NotFoundError:
        raise
    except Exception as e:
        await session.rollback()
        logger.exception("Error deleting note with id=%s", note_id, stack_info=True)
        raise DatabaseError from e


async def search_notes_by_text_vector(
    session: AsyncSession, query_vector: Tensor,limit:int
) -> list[tuple[Note, float]]:
    try:
        # Label the similarity score
        similarity_expr = (1 - Note.embedding.cosine_distance(query_vector)).label(
            "similarity_score"
        )

        query = (
            select(Note, similarity_expr)
            .order_by(similarity_expr.desc())  # order by highest similarity
            .limit(limit)
        )

        response: ScalarResult = await session.execute(query)
        notes: Sequence[tuple[Note, float]] = response.all()

        return notes
    except Exception as e:
        logger.exception("Error while searching note", stack_info=True)
        raise DatabaseError from e
