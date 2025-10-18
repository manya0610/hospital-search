from sentence_transformers import SentenceTransformer

# Load a pre-trained model (you can choose many others — see below)
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

# Example text
text = "The quick brown fox jumps over the lazy dog."


def get_embeddings(text: str):
    # Create embedding vector
    return model.encode(text, normalize_embeddings=True)
