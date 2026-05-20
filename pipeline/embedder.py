"""
Loads a local sentence-transformer model and produces embeddings for text chunks.
Using all-MiniLM-L6-v2: fast, 384-dim, no API key required.
"""
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

_model = None


def get_model():
    global _model
    if _model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL} ...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print("Model loaded.")
    return _model


def embed(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    return embeddings.tolist()
