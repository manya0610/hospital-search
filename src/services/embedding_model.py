import logging

from sentence_transformers import SentenceTransformer
from torch import Tensor

from src.exceptions.other_exceptions import EmbeddingError

logging.basicConfig()
logger = logging.getLogger(__name__)

# Load a pre-trained model (you can choose many others — see below)
text_embedding_model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")


def get_embeddings(text: str) -> Tensor:
    # Create embedding
    try:
        return text_embedding_model.encode(text, normalize_embeddings=True)
    except Exception as e:
        logger.exception("Exception while creating embedding for text %s,", text)
        raise EmbeddingError from e
