from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Note
from src.repo import note_repo
from src.services.embedding_model import get_embeddings


async def search_notes_by_text(
    session: AsyncSession, text: str
) -> list[tuple[Note, float]]:
    embedding = get_embeddings(text)
    return await note_repo.search_notes_by_text_vector(session, embedding)
